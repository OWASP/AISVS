<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C10-MCP-Security.md -->
<!-- Translator: GeeksikhSecurity -->

# C10 Model Context Protocol (MCP) Security
# C10 Model Context Protocol (MCP)[^0x10-C10-mcp] ਸੁਰੱਖਿਆ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses secure discovery, authentication, authorization, transport, and use of MCP-based tool and resource integrations.

ਇਹ ਅਧਿਆਇ MCP-ਆਧਾਰਿਤ ਟੂਲ ਅਤੇ ਸਰੋਤ ਏਕੀਕਰਨਾਂ (integrations) ਦੀ ਸੁਰੱਖਿਅਤ ਖੋਜ[^0x10-C10-discovery] (discovery), ਪ੍ਰਮਾਣੀਕਰਨ, ਅਧਿਕਾਰੀਕਰਨ, ਟ੍ਰਾਂਸਪੋਰਟ[^0x10-C10-transport], ਅਤੇ ਵਰਤੋਂ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ।

---

## C10.1 Component Integrity
## C10.1 ਕੰਪੋਨੈਂਟ[^0x10-C10-component] ਅਖੰਡਤਾ

Only trusted MCP components must be used, and locally launched servers must be secured.

ਸਿਰਫ਼ ਭਰੋਸੇਯੋਗ MCP ਕੰਪੋਨੈਂਟਾਂ ਦੀ ਹੀ ਵਰਤੋਂ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਚਾਲੂ ਕੀਤੇ ਗਏ ਸਰਵਰਾਂ[^0x10-C10-server] ਨੂੰ ਸੁਰੱਖਿਅਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **10.1.1** | **Verify that** MCP components are obtained only from trusted sources and cryptographically verified. | 1 |
| **10.1.2** | **Verify that** only allow-listed MCP servers are permitted. | 2 |
| **10.1.3** | **Verify that** locally launched MCP servers run in a least-privilege sandbox with restricted file system, network, and system access. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **10.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਕੰਪੋਨੈਂਟ ਸਿਰਫ਼ ਭਰੋਸੇਯੋਗ ਸਰੋਤਾਂ ਤੋਂ ਹੀ ਪ੍ਰਾਪਤ ਕੀਤੇ ਜਾਂਦੇ ਹਨ ਅਤੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਤਸਦੀਕ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 1 |
| **10.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਰਫ਼ allow-list ਵਿੱਚ ਸ਼ਾਮਲ MCP ਸਰਵਰਾਂ ਦੀ ਹੀ ਆਗਿਆ ਹੈ। | 2 |
| **10.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਚਾਲੂ ਕੀਤੇ ਗਏ MCP ਸਰਵਰ ਸੀਮਤ ਫ਼ਾਈਲ ਸਿਸਟਮ, ਨੈੱਟਵਰਕ, ਅਤੇ ਸਿਸਟਮ ਪਹੁੰਚ ਵਾਲੇ ਘੱਟੋ-ਘੱਟ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ (least-privilege) ਸੈਂਡਬਾਕਸ ਵਿੱਚ ਚੱਲਦੇ ਹਨ। | 2 |

---

## C10.2 Authentication & Authorization
## C10.2 ਪ੍ਰਮਾਣੀਕਰਨ ਅਤੇ ਅਧਿਕਾਰੀਕਰਨ

Callers must be authenticated and access to MCP servers authorized, following protocol best practices.

ਪ੍ਰੋਟੋਕੋਲ ਦੇ ਬਿਹਤਰੀਨ ਅਮਲਾਂ ਦੀ ਪਾਲਣਾ ਕਰਦਿਆਂ, ਸੱਦਣ ਵਾਲਿਆਂ (callers) ਦਾ ਪ੍ਰਮਾਣੀਕਰਨ ਹੋਣਾ ਅਤੇ MCP ਸਰਵਰਾਂ ਤੱਕ ਪਹੁੰਚ ਦਾ ਅਧਿਕਾਰੀਕਰਨ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **10.2.1** | **Verify that** MCP servers validate access tokens for each request and do not rely on transport security alone. | 1 |
| **10.2.2** | **Verify that** MCP servers validate the presented access token's issuer, audience, expiration, and scope claims in accordance with OAuth 2.1. | 1 |
| **10.2.3** | **Verify that** MCP servers acting as OAuth 2.1 resource servers do not store or persist access tokens or user credentials. | 1 |
| **10.2.4** | **Verify that** MCP tools/list returns only tools permitted by resource owners' authorized scopes. | 2 |
| **10.2.5** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 |
| **10.2.6** | **Verify that** MCP servers ensure all session artifacts are removed when a session terminates. | 2 |
| **10.2.7** | **Verify that** MCP servers do not pass through access tokens received from clients to downstream APIs. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **10.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ ਹਰ ਬੇਨਤੀ ਲਈ ਪਹੁੰਚ ਟੋਕਨ ਪ੍ਰਮਾਣਿਤ ਕਰਦੇ ਹਨ ਅਤੇ ਇਕੱਲੀ ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ 'ਤੇ ਨਿਰਭਰ ਨਹੀਂ ਕਰਦੇ। | 1 |
| **10.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ ਪੇਸ਼ ਕੀਤੇ ਗਏ ਪਹੁੰਚ ਟੋਕਨ ਦੇ ਜਾਰੀਕਰਤਾ (issuer), ਉਦੇਸ਼ਿਤ ਪ੍ਰਾਪਤਕਰਤਾ[^0x10-C10-audience] (audience), ਮਿਆਦ ਸਮਾਪਤੀ (expiration), ਅਤੇ ਸਕੋਪ ਦੇ ਦਾਅਵਿਆਂ (claims) ਨੂੰ OAuth 2.1 ਦੇ ਅਨੁਸਾਰ ਪ੍ਰਮਾਣਿਤ ਕਰਦੇ ਹਨ। | 1 |
| **10.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** OAuth 2.1 ਸਰੋਤ ਸਰਵਰਾਂ (resource servers) ਵਜੋਂ ਕੰਮ ਕਰਨ ਵਾਲੇ MCP ਸਰਵਰ ਪਹੁੰਚ ਟੋਕਨ ਜਾਂ ਉਪਭੋਗਤਾ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਨਾ ਤਾਂ ਭੰਡਾਰ ਕਰਦੇ ਹਨ ਅਤੇ ਨਾ ਹੀ ਸਥਾਈ ਤੌਰ 'ਤੇ ਰੱਖਦੇ ਹਨ। | 1 |
| **10.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP `tools/list` ਸਿਰਫ਼ ਉਹੀ ਟੂਲ ਵਾਪਸ ਕਰਦਾ ਹੈ ਜਿਨ੍ਹਾਂ ਦੀ ਸਰੋਤ ਮਾਲਕਾਂ (resource owners) ਦੇ ਅਧਿਕਾਰਤ ਸਕੋਪਾਂ ਦੁਆਰਾ ਆਗਿਆ ਹੈ। | 2 |
| **10.2.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ ਹਰ ਟੂਲ ਸੱਦੇ (tool invocation) 'ਤੇ ਪਹੁੰਚ ਕੰਟਰੋਲ ਲਾਗੂ ਕਰਦੇ ਹਨ, ਅਤੇ ਇਹ ਪ੍ਰਮਾਣਿਤ ਕਰਦੇ ਹਨ ਕਿ ਉਪਭੋਗਤਾ ਦਾ ਪਹੁੰਚ ਟੋਕਨ ਬੇਨਤੀ ਕੀਤੇ ਟੂਲ ਅਤੇ ਦਿੱਤੇ ਗਏ ਖ਼ਾਸ ਆਰਗੂਮੈਂਟ ਮੁੱਲਾਂ, ਦੋਵਾਂ ਦਾ ਅਧਿਕਾਰੀਕਰਨ ਕਰਦਾ ਹੈ। | 2 |
| **10.2.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ ਇਹ ਯਕੀਨੀ ਬਣਾਉਂਦੇ ਹਨ ਕਿ ਜਦੋਂ ਕੋਈ ਸੈਸ਼ਨ ਸਮਾਪਤ ਹੁੰਦਾ ਹੈ ਤਾਂ ਸਾਰੇ ਸੈਸ਼ਨ ਆਰਟੀਫ਼ੈਕਟ ਹਟਾ ਦਿੱਤੇ ਜਾਂਦੇ ਹਨ। | 2 |
| **10.2.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ ਕਲਾਇੰਟਾਂ ਤੋਂ ਪ੍ਰਾਪਤ ਹੋਏ ਪਹੁੰਚ ਟੋਕਨ ਡਾਊਨਸਟ੍ਰੀਮ[^0x10-C10-downstream] API ਨੂੰ ਅੱਗੇ ਨਹੀਂ ਲੰਘਾਉਂਦੇ[^0x10-C10-passthrough] (pass through)। | 2 |

---

## C10.3 Secure Transport
## C10.3 ਸੁਰੱਖਿਅਤ ਟ੍ਰਾਂਸਪੋਰਟ

MCP communications must be secured following protocol best practices.

ਪ੍ਰੋਟੋਕੋਲ ਦੇ ਬਿਹਤਰੀਨ ਅਮਲਾਂ ਦੀ ਪਾਲਣਾ ਕਰਦਿਆਂ MCP ਸੰਚਾਰਾਂ ਨੂੰ ਸੁਰੱਖਿਅਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **10.3.1** | **Verify that** authenticated, encrypted streamable HTTP is used for MCP transport for remote services. | 1 |
| **10.3.2** | **Verify that** stdio transport is permitted only in controlled local environments. | 1 |
| **10.3.3** | **Verify that** MCP servers validate both the Origin header and the Host header independently on all HTTP-based transports to prevent DNS rebinding attacks. | 2 |
| **10.3.4** | **Verify that** MCP clients enforce a minimum acceptable protocol version and reject initialize responses that propose a version below that minimum. | 2 |
| **10.3.5** | **Verify that** access tokens between the MCP client and server are sender-constrained using mTLS or DPoP. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **10.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਰਿਮੋਟ ਸੇਵਾਵਾਂ ਲਈ MCP ਟ੍ਰਾਂਸਪੋਰਟ ਵਾਸਤੇ ਪ੍ਰਮਾਣੀਕਰਨ ਕੀਤਾ ਗਿਆ, ਏਨਕ੍ਰਿਪਟ ਕੀਤਾ ਗਿਆ streamable HTTP ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ। | 1 |
| **10.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** stdio ਟ੍ਰਾਂਸਪੋਰਟ ਦੀ ਆਗਿਆ ਸਿਰਫ਼ ਨਿਯੰਤਰਿਤ ਸਥਾਨਕ ਵਾਤਾਵਰਣਾਂ ਵਿੱਚ ਹੀ ਹੈ। | 1 |
| **10.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ DNS rebinding[^0x10-C10-replay-dns] ਹਮਲਿਆਂ ਨੂੰ ਰੋਕਣ ਲਈ ਸਾਰੇ HTTP-ਆਧਾਰਿਤ ਟ੍ਰਾਂਸਪੋਰਟਾਂ ਉੱਤੇ `Origin` ਹੈੱਡਰ ਅਤੇ `Host` ਹੈੱਡਰ ਦੋਵਾਂ ਨੂੰ ਵੱਖਰੇ ਤੌਰ 'ਤੇ ਪ੍ਰਮਾਣਿਤ ਕਰਦੇ ਹਨ। | 2 |
| **10.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਕਲਾਇੰਟ ਇੱਕ ਘੱਟੋ-ਘੱਟ ਸਵੀਕਾਰਯੋਗ ਪ੍ਰੋਟੋਕੋਲ ਸੰਸਕਰਣ ਲਾਗੂ ਕਰਦੇ ਹਨ ਅਤੇ ਉਹਨਾਂ `initialize` ਜਵਾਬਾਂ ਨੂੰ ਰੱਦ ਕਰਦੇ ਹਨ ਜੋ ਉਸ ਘੱਟੋ-ਘੱਟ ਤੋਂ ਹੇਠਲਾ ਸੰਸਕਰਣ ਪ੍ਰਸਤਾਵਿਤ ਕਰਦੇ ਹਨ। | 2 |
| **10.3.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਕਲਾਇੰਟ ਅਤੇ ਸਰਵਰ ਵਿਚਕਾਰਲੇ ਪਹੁੰਚ ਟੋਕਨ mTLS ਜਾਂ DPoP ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਭੇਜਣ ਵਾਲੇ ਨਾਲ ਬੰਨ੍ਹੇ ਹੋਏ[^0x10-C10-sender-constrained] (sender-constrained) ਹਨ। | 3 |

---

## C10.4 Schema, Message, and Input Validation
## C10.4 ਸਕੀਮਾ, ਸੁਨੇਹਾ, ਅਤੇ ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ

Schema, message, and input validation must be enforced in both MCP servers and clients.

MCP ਸਰਵਰਾਂ ਅਤੇ ਕਲਾਇੰਟਾਂ, ਦੋਵਾਂ ਵਿੱਚ ਸਕੀਮਾ, ਸੁਨੇਹਾ, ਅਤੇ ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ ਲਾਗੂ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **10.4.1** | **Verify that** MCP tools/list and tools/call responses are validated against their declared schemas before being injected into the model context. | 1 |
| **10.4.2** | **Verify that** MCP tools/list and tools/call responses are screened for indirect prompt injection before being injected into the model context. | 1 |
| **10.4.3** | **Verify that** MCP servers reject unrecognized or oversized parameters in function calls. | 1 |
| **10.4.4** | **Verify that** all MCP servers enforce strict schema validation. | 2 |
| **10.4.5** | **Verify that** all MCP transports enforce maximum payload size limits. | 2 |
| **10.4.6** | **Verify that** MCP servers sign tool responses with a unique nonce and timestamp so MCP clients can detect replay attempts. | 2 |
| **10.4.7** | **Verify that** MCP clients present users with explicit consent dialogue and cancellation options upon installation of a local MCP server. | 2 |
| **10.4.8** | **Verify that** MCP clients maintain a snapshot of tool definitions and that any change to a tool definition triggers re-approval before the modified tool can be invoked. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **10.4.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP `tools/list` ਅਤੇ `tools/call` ਜਵਾਬਾਂ ਨੂੰ ਮਾਡਲ ਸੰਦਰਭ ਵਿੱਚ ਇੰਜੈਕਟ ਕੀਤੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਉਹਨਾਂ ਦੀਆਂ ਘੋਸ਼ਿਤ ਸਕੀਮਾਵਾਂ ਦੇ ਵਿਰੁੱਧ ਪ੍ਰਮਾਣਿਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **10.4.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP `tools/list` ਅਤੇ `tools/call` ਜਵਾਬਾਂ ਦੀ, ਮਾਡਲ ਸੰਦਰਭ ਵਿੱਚ ਇੰਜੈਕਟ ਕੀਤੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ, ਅਸਿੱਧੇ prompt ਇੰਜੈਕਸ਼ਨ (indirect prompt injection) ਲਈ ਛਾਣਬੀਣ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 1 |
| **10.4.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ ਫ਼ੰਕਸ਼ਨ ਕਾਲਾਂ ਵਿੱਚ ਅਣਪਛਾਤੇ ਜਾਂ ਲੋੜੋਂ ਵੱਡੇ ਪੈਰਾਮੀਟਰਾਂ ਨੂੰ ਰੱਦ ਕਰਦੇ ਹਨ। | 1 |
| **10.4.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਾਰੇ MCP ਸਰਵਰ ਸਖ਼ਤ ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ ਲਾਗੂ ਕਰਦੇ ਹਨ। | 2 |
| **10.4.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਾਰੇ MCP ਟ੍ਰਾਂਸਪੋਰਟ ਵੱਧ ਤੋਂ ਵੱਧ ਪੇਲੋਡ ਆਕਾਰ ਸੀਮਾਵਾਂ ਲਾਗੂ ਕਰਦੇ ਹਨ। | 2 |
| **10.4.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਸਰਵਰ ਟੂਲ ਜਵਾਬਾਂ ਉੱਤੇ ਇੱਕ ਵਿਲੱਖਣ ਨੌਂਸ (nonce) ਅਤੇ ਟਾਈਮਸਟੈਂਪ ਨਾਲ ਦਸਤਖ਼ਤ ਕਰਦੇ ਹਨ ਤਾਂ ਜੋ MCP ਕਲਾਇੰਟ replay[^0x10-C10-replay-dns] (ਦੁਹਰਾਓ) ਕੋਸ਼ਿਸ਼ਾਂ ਦਾ ਪਤਾ ਲਗਾ ਸਕਣ। | 2 |
| **10.4.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਕਲਾਇੰਟ ਕਿਸੇ ਸਥਾਨਕ MCP ਸਰਵਰ ਦੀ ਸਥਾਪਨਾ ਵੇਲੇ ਉਪਭੋਗਤਾਵਾਂ ਸਾਹਮਣੇ ਸਪੱਸ਼ਟ ਸਹਿਮਤੀ ਸੰਵਾਦ[^0x10-C10-consent] (consent dialogue) ਅਤੇ ਰੱਦ ਕਰਨ ਦੇ ਵਿਕਲਪ ਪੇਸ਼ ਕਰਦੇ ਹਨ। | 2 |
| **10.4.8** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** MCP ਕਲਾਇੰਟ ਟੂਲ ਪਰਿਭਾਸ਼ਾਵਾਂ ਦਾ ਇੱਕ ਸਨੈਪਸ਼ਾਟ ਬਰਕਰਾਰ ਰੱਖਦੇ ਹਨ, ਅਤੇ ਕਿਸੇ ਟੂਲ ਪਰਿਭਾਸ਼ਾ ਵਿੱਚ ਕੋਈ ਵੀ ਤਬਦੀਲੀ ਹੋਣ 'ਤੇ, ਸੋਧਿਆ ਹੋਇਆ ਟੂਲ ਸੱਦੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਮੁੜ-ਮਨਜ਼ੂਰੀ ਸ਼ੁਰੂ ਹੁੰਦੀ ਹੈ। | 3 |

---

## References
## ਹਵਾਲੇ

* [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
* [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [OAuth 2.1 (IETF Draft)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-11)
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)

[^0x10-C10-mcp]: **Model Context Protocol (MCP)** (EN) -> retained verbatim — kept in English/Latin because it is the wire protocol's proper name and a reader must be able to match it against the specification this chapter cites. Full discussion: OPEN-QUESTIONS.md Q87.
[^0x10-C10-discovery]: **discovery** (EN) -> ਖੋਜ — reuses a word already carrying *lookup/search* elsewhere in the corpus; flagged as a known overload rather than a fresh coinage. Full discussion: OPEN-QUESTIONS.md Q94.
[^0x10-C10-component]: **component** (EN) -> ਕੰਪੋਨੈਂਟ — logged as an open corpus split: C09/C10 use this loan while C03/C04/C12 use the native ਹਿੱਸਾ for the identical term-of-art sense. Full discussion: OPEN-QUESTIONS.md Q95.
[^0x10-C10-server]: **server / client** (EN) -> ਸਰਵਰ / ਕਲਾਇੰਟ — the devotional-toned ਸੇਵਾਦਾਰ ("one who serves") was excluded because ਸੇਵਾ is load-bearing Gurmat vocabulary for selfless service. Full discussion: OPEN-QUESTIONS.md Q88.
[^0x10-C10-transport]: **transport** (EN) -> ਟ੍ਰਾਂਸਪੋਰਟ — kept as a loan over literal "haulage" renderings, which would suggest physical goods rather than a protocol channel. Full discussion: OPEN-QUESTIONS.md Q90.
[^0x10-C10-audience]: **audience** (token claim) (EN) -> ਉਦੇਸ਼ਿਤ ਪ੍ਰਾਪਤਕਰਤਾ ("intended recipient") — chosen over ਸਰੋਤੇ/ਦਰਸ਼ਕ ("listening/viewing public"), which would invert the OAuth meaning of a single intended token recipient. Full discussion: OPEN-QUESTIONS.md Q89.
[^0x10-C10-downstream]: **downstream** (EN) -> ਡਾਊਨਸਟ੍ਰੀਮ — kept as a loan, consistent with the corpus's other pipeline/infrastructure loans, rather than a literal water-flow rendering. Full discussion: OPEN-QUESTIONS.md Q77.
[^0x10-C10-passthrough]: **pass through** (EN) -> ਅੱਗੇ ਲੰਘਾਉਣਾ — deliberately kept distinct from ਅੱਗੇ ਸੰਚਾਰਿਤ ਕਰਨਾ (C09's *approved* delegation-token propagation) so a prohibition and an obligation don't read as the same act. Full discussion: OPEN-QUESTIONS.md Q101.
[^0x10-C10-replay-dns]: **DNS rebinding / replay** (EN) -> `DNS rebinding` retained verbatim; `replay` retained with a ਦੁਹਰਾਓ ("repetition") gloss — both are named attack classes kept searchable against the cited OWASP MCP Security Cheat Sheet. Full discussion: OPEN-QUESTIONS.md Q92.
[^0x10-C10-sender-constrained]: **sender-constrained** (EN) -> ਭੇਜਣ ਵਾਲੇ ਨਾਲ ਬੰਨ੍ਹੇ ਹੋਏ — reuses the corpus's existing verb for cryptographic binding (ਬੰਨ੍ਹਣਾ) rather than ਸੀਮਿਤ, which would suggest scope-restriction, a different control. Full discussion: OPEN-QUESTIONS.md Q91.
[^0x10-C10-consent]: **consent dialogue** (EN) -> ਸਪੱਸ਼ਟ ਸਹਿਮਤੀ ਸੰਵਾਦ — ਮਨਜ਼ੂਰੀ ("approval") was deliberately avoided because 10.4.8 already locks it to *re-approval*, and consent and re-approval are two separate obligations in this same section. Full discussion: OPEN-QUESTIONS.md Q93.
