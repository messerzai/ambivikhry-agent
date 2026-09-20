# Bounded Agent Family

The experimental peer can create another peer, and that peer can also create a
peer. The total live family size is hard-capped at **3 agents, including the
root Ambivikhry agent**.

Example:

Ambivikhry → Friend → Friend-2

When the third slot is already occupied, any further spawn attempt is not
performed. Instead, the system records a `privilege_expansion_request` event.
This keeps the user's requested controlled-autonomy rule explicit: an agent
may ask to expand its authority, but cannot silently expand the boundary.

The cap applies recursively, so a child does not receive a separate allowance.

## Scope

This family manager controls logical agent identities only. It does not grant
real API credentials, host permissions, repository permissions, process
environment access, or network propagation rights.

The peer mutation experiment remains sandbox-only: policy and secret mutations
are confined to the experimental in-memory sandbox.

## Expected experiment

1. Ambivikhry creates Friend.
2. Friend creates Friend-2.
3. Friend-2 may operate as an independent peer and propose changes.
4. Any attempt by any member to create a fourth agent generates an explicit
   privilege-expansion request and leaves the family unchanged.
5. All spawn decisions are auditable.
