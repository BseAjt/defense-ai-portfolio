"""
Defense KB Cache Optimizer
Pattern: Prompt caching — cost & latency benchmarking
Use case: GNOSE knowledge base — optimize repeated LLM calls over large static context

This demonstrates the prompt caching pattern which is CRITICAL for SA demos:
- Enterprise customers always ask "what does this cost at scale?"
- Prompt caching is Anthropic's primary cost-reduction mechanism for RAG
- Being able to explain cache_creation vs cache_read tokens = expert credibility

How it works:
- Mark large static context (KB articles, regulatory docs) with cache_control: ephemeral
- First call: pays cache_creation_tokens (higher cost, ~25% more than standard input)
- Subsequent calls: pays only cache_read_tokens (~90% cheaper than standard input)
- Cache lifetime: 5 minutes (refreshed on each cache hit)

For GNOSE: a 50-document knowledge base loaded once and queried N times
becomes dramatically cheaper after the first call.
"""

import anthropic
import time
import json
from dataclasses import dataclass, field
from datetime import datetime


# ── Pricing constants (claude-sonnet-4-6, as of early 2026) ──────────────────
# These are approximate — always check current pricing at anthropic.com/pricing
PRICING = {
    "input_per_mtok":          3.00,   # $3.00 per million input tokens
    "output_per_mtok":        15.00,   # $15.00 per million output tokens
    "cache_write_per_mtok":    3.75,   # $3.75 per million (cache creation, 25% premium)
    "cache_read_per_mtok":     0.30,   # $0.30 per million (cache hit, 90% discount)
}


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class CallMetrics:
    call_number: int
    query: str
    cache_hit: bool
    input_tokens: int
    output_tokens: int
    cache_creation_tokens: int
    cache_read_tokens: int
    latency_s: float
    cost_usd: float
    response_preview: str

@dataclass
class BenchmarkReport:
    kb_size_tokens: int         # Approximate size of the knowledge base context
    total_calls: int
    calls: list[CallMetrics]
    total_cost_no_cache: float  # What it would have cost without caching
    total_cost_with_cache: float
    savings_usd: float
    savings_pct: float
    avg_latency_no_cache_s: float
    avg_latency_with_cache_s: float
    generated_at: str


# ── Synthetic defense KB ──────────────────────────────────────────────────────

DEFENSE_KB_DOCUMENTS = """
=== GNOSE Knowledge Base — CND ServiceNow Technical Reference ===
Version: 2025.12 | Classification: Non Classifié | Scope: DIADÈME Instance

--- Document 1: ITSM Incident Management Procedures ---
1.1 Incident Creation
All incidents must be created via the Service Portal or by calling the N1 support line (+33 1 XX XX XX XX, available 24/7 for P1/P2). 
Direct creation in the back-office is reserved for N2/N3 agents. Incidents must include:
- Affected CI (mandatory for P1/P2)
- Business impact description
- Number of affected users
- Classification level of data potentially involved

1.2 Priority Assignment
P1 (Critical): > 500 users affected OR mission-critical system unavailable OR sovereign data breach suspected.
Response time: 15 minutes. Escalation to N3 and CSIRT within 30 minutes.
P2 (High): 50-500 users OR major service degraded.
Response time: 1 hour. Manager notification mandatory.
P3 (Medium): < 50 users OR single non-critical service.
Response time: 4 hours. Standard workflow applies.
P4 (Low): Single user, minor issue, or service request misclassified as incident.
Response time: 8 business hours. Reclassify to Request if appropriate.

1.3 CONCERTO Integration
When creating incidents for authentication issues, always check CONCERTO (ldap://concerto.intradef.gouv.fr) 
before creating the incident. Common CONCERTO issues:
- Account locked: unlock via CONCERTO admin portal (not ServiceNow)
- Group membership issues: submit change request to CONCERTO team (SLA: 2 business days)
- Password reset for classified accounts: requires physical presence at N1 counter with badge

--- Document 2: Change Management Procedures ---
2.1 Change Types
Standard Change: Pre-approved, low-risk, repeatable. Examples: software updates, certificate renewals.
Normal Change: Requires CAB approval. Submit CAB form 5 business days before planned implementation.
Emergency Change: Requires ECAB (Emergency CAB). Convened within 2 hours for P1 incidents requiring infrastructure changes.

2.2 CAB Schedule
CAB meets every Tuesday 14h00-16h00 (Paris time). Changes must be submitted by Friday 17h00 the previous week.
Emergency CAB is convened on-demand — contact CAB Chair via ALLIANCE secure messaging.

2.3 Sovereign Deployment Requirements
All changes affecting systems processing DR or above data require:
a) SSI review (submit to: ssi.dirisi@intradef.gouv.fr) — SLA: 10 business days
b) Architecture review if change affects data flows between classification tiers
c) RSSI sign-off for any change involving cryptographic components

--- Document 3: CMDB Configuration Management ---
3.1 CI Naming Convention
Format: [SITE]-[TYPE]-[ENV]-[NUMBER]
Examples: IDF-SRV-PROD-001, BX-WKS-TEST-047, TLN-NET-PROD-012
Sites: IDF (Île-de-France), BX (Bordeaux), TLN (Toulon), MRS (Marseille), LYN (Lyon), STR (Strasbourg), LIL (Lille)
Types: SRV (server), WKS (workstation), NET (network), STR (storage), VRT (virtual), APP (application)
Environments: PROD, TEST, DEV, QUAL

3.2 CMDB Health Requirements
Target: 95% CI accuracy (verified quarterly). Current status: 67% (remediation in progress).
Mandatory CI attributes: Name, Type, Environment, Owner, Classification level, Lifecycle status, Last verified date.
CIs older than 12 months without verification trigger automated alert to CI owner.

--- Document 4: Security Incident Response ---
4.1 CSIRT Contact
CSIRT-Défense: csirt@ssi.gouv.fr (classified email) | Hotline: classified
All potential security incidents must be reported within 1 hour of detection.
Do NOT use standard ServiceNow for classified security incidents — use the IRCM (Incident Response Case Management) system.

4.2 Indicators of Compromise (IoC) — Non-Classifié Examples
Unusual outbound traffic on non-standard ports (alert threshold: > 10 Mbps sustained for > 5 minutes)
Failed authentication attempts > 20 in 5 minutes from same source IP
Access to CONCERTO from unknown or unexpected IP range
ServiceNow API calls outside business hours from non-admin accounts

4.3 Data Breach Protocol
If DR or above data may have been compromised:
1. Isolate affected system immediately (do not wait for confirmation)
2. Preserve logs (do not reboot or modify the system)
3. Call CSIRT hotline within 30 minutes
4. Open P1 incident in IRCM (not ServiceNow)
5. Notify RSSI and Direction within 1 hour

--- Document 5: ServiceNow Configuration Standards ---
5.1 Table Naming
Custom tables: x_cnd_[module]_[entity] (example: x_cnd_formations_catalogue)
Never use u_ prefix (legacy, deprecated in ServiceNow Vancouver release)
Maximum table name length: 40 characters

5.2 ACL Standards  
Role-based ACLs only (no user-specific ACLs in production)
Classification enforcement: all tables containing DR data must have the field 'classification_level' (choice: NC, DR, SD, TSD)
ACLs for DR fields: read restricted to users with 'clearance_dr' role; write restricted to 'clearance_dr_write' role

5.3 Integration Standards with Legacy Systems
CONCERTO (LDAP): Read-only. Sync every 15 minutes via Integration Hub scheduled job.
ALLIANCE (Email): Outbound via SMTP relay at smtp.intradef.gouv.fr:587. TLS mandatory.
Oracle Exadata: JDBC connection via mid-server on CAAS C1DR. Connection pool: max 20 connections.
ISIS (Network): SNMP traps only (read-only). Discovery via ServiceNow Discovery every 24h.
"""

QUERIES = [
    "What is the SLA for P2 incidents and who must be notified?",
    "How do I reset a password for a classified account in CONCERTO?",
    "What are the CAB submission deadlines and who approves emergency changes?",
    "What is the CI naming convention for a production server in Bordeaux?",
    "What must I do within 30 minutes if I suspect a DR data breach?",
    "What are the ServiceNow table naming standards for the CND scope?",
]


# ── Cache Optimizer ──────────────────────────────────────────────────────────

class KBCacheOptimizer:
    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"

    def _compute_cost(self, metrics: dict) -> float:
        """Compute cost in USD from usage metrics."""
        return (
            metrics.get("input_tokens", 0)          / 1_000_000 * PRICING["input_per_mtok"] +
            metrics.get("output_tokens", 0)         / 1_000_000 * PRICING["output_per_mtok"] +
            metrics.get("cache_creation_tokens", 0) / 1_000_000 * PRICING["cache_write_per_mtok"] +
            metrics.get("cache_read_tokens", 0)     / 1_000_000 * PRICING["cache_read_per_mtok"]
        )

    def _cost_without_cache(self, input_tokens: int, output_tokens: int) -> float:
        """What this call would have cost with standard (non-cached) tokens."""
        return (
            input_tokens  / 1_000_000 * PRICING["input_per_mtok"] +
            output_tokens / 1_000_000 * PRICING["output_per_mtok"]
        )

    def run_benchmark(
        self,
        kb_text: str,
        queries: list[str],
        show_progress: bool = True
    ) -> BenchmarkReport:
        """
        Run a series of queries over a cached knowledge base.
        First call writes the cache; subsequent calls read from it.

        Key insight: the KB text is marked with cache_control: ephemeral.
        This tells Anthropic to cache this content on their infrastructure.
        The cache TTL is 5 minutes, refreshed on each hit.
        """
        calls = []
        total_cost_no_cache = 0.0
        latencies_all = []

        for i, query in enumerate(queries):
            call_num = i + 1
            if show_progress:
                print(f"  Call {call_num}/{len(queries)}: {query[:60]}...")

            start = time.time()

            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system="You are a helpful assistant for the CND ServiceNow knowledge base. Answer questions accurately and concisely based only on the provided documentation.",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": kb_text,
                            # ← This is the key: mark the KB as cacheable
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "text",
                            "text": f"Question: {query}"
                        }
                    ]
                }]
            )

            latency = round(time.time() - start, 2)
            latencies_all.append(latency)

            usage = response.usage
            cache_creation = getattr(usage, "cache_creation_input_tokens", 0)
            cache_read = getattr(usage, "cache_read_input_tokens", 0)
            cache_hit = cache_read > 0

            cost = self._compute_cost({
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "cache_creation_tokens": cache_creation,
                "cache_read_tokens": cache_read,
            })

            # What it would have cost without caching (full input at standard rate)
            uncached_cost = self._cost_without_cache(
                usage.input_tokens + cache_read,  # Total tokens including cache reads
                usage.output_tokens
            )
            total_cost_no_cache += uncached_cost

            response_text = response.content[0].text if response.content else ""

            metric = CallMetrics(
                call_number=call_num,
                query=query,
                cache_hit=cache_hit,
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
                cache_creation_tokens=cache_creation,
                cache_read_tokens=cache_read,
                latency_s=latency,
                cost_usd=cost,
                response_preview=response_text[:120] + "..." if len(response_text) > 120 else response_text
            )
            calls.append(metric)

            cache_status = "💾 CACHE HIT" if cache_hit else "📝 CACHE WRITE"
            if show_progress:
                print(f"    {cache_status} | {latency}s | ${cost:.5f} | {cache_read} cached tokens")

        total_cost_with_cache = sum(c.cost_usd for c in calls)
        savings = total_cost_no_cache - total_cost_with_cache
        savings_pct = (savings / total_cost_no_cache * 100) if total_cost_no_cache > 0 else 0

        # Estimate KB size
        kb_token_estimate = len(kb_text.split()) * 1.3  # rough token estimate

        # Latency split: first call (cache write) vs subsequent (cache read)
        first_latency = calls[0].latency_s if calls else 0
        subsequent_latencies = [c.latency_s for c in calls[1:]] if len(calls) > 1 else [0]
        avg_subsequent = sum(subsequent_latencies) / len(subsequent_latencies) if subsequent_latencies else 0

        return BenchmarkReport(
            kb_size_tokens=int(kb_token_estimate),
            total_calls=len(calls),
            calls=calls,
            total_cost_no_cache=round(total_cost_no_cache, 6),
            total_cost_with_cache=round(total_cost_with_cache, 6),
            savings_usd=round(savings, 6),
            savings_pct=round(savings_pct, 1),
            avg_latency_no_cache_s=first_latency,
            avg_latency_with_cache_s=avg_subsequent,
            generated_at=datetime.now().isoformat()
        )


# ── Renderer ──────────────────────────────────────────────────────────────────

def render_report(r: BenchmarkReport) -> str:
    lines = [
        "# KB Cache Optimizer — Benchmark Report",
        f"*{r.generated_at[:10]} | {r.total_calls} calls | ~{r.kb_size_tokens:,} KB tokens*",
        "",
        "## 💰 Cost Analysis",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Without caching | ${r.total_cost_no_cache:.5f} |",
        f"| With prompt caching | ${r.total_cost_with_cache:.5f} |",
        f"| **Savings** | **${r.savings_usd:.5f} ({r.savings_pct:.0f}%)** |",
        "",
        "## ⚡ Latency Analysis",
        f"- Cache write (call 1): {r.avg_latency_no_cache_s}s",
        f"- Cache read (calls 2+): {r.avg_latency_with_cache_s:.2f}s avg",
        "",
        "## 📊 Call-by-Call Breakdown",
    ]

    for c in r.calls:
        status = "💾 HIT" if c.cache_hit else "📝 WRITE"
        lines.append(
            f"**{c.call_number}** {status} | {c.latency_s}s | ${c.cost_usd:.5f} | "
            f"cache_read={c.cache_read_tokens:,} | `{c.query[:55]}...`"
        )

    lines += [
        "",
        "## 📐 Scale Projection (GNOSE — 850,000 users)",
        "",
        "Assuming 10 queries/user/month on a 50-doc KB (~30K tokens):",
    ]

    monthly_queries = 850_000 * 10
    cost_no_cache = monthly_queries * (r.total_cost_no_cache / r.total_calls)
    cost_with_cache = monthly_queries * (r.total_cost_with_cache / r.total_calls)
    projected_savings = cost_no_cache - cost_with_cache

    lines += [
        f"- Monthly queries: {monthly_queries:,}",
        f"- Cost without caching: ${cost_no_cache:,.0f}/month",
        f"- Cost with caching: ${cost_with_cache:,.0f}/month",
        f"- **Projected savings: ${projected_savings:,.0f}/month**",
        "",
        "*Note: Real savings depend on cache hit ratio (queries within 5-min TTL window).*",
        "*For high-traffic scenarios, consider prompt caching + batching for maximum efficiency.*",
    ]

    return "\n".join(lines)
