---
id: overview
title: System Design
sidebar_position: 1
slug: /system-design/overview
status: in_progress
---

# System Design

Principal-level system design exercises and decision frameworks.

```mermaid
flowchart LR
    Req[Requirements] --> Scale[Scale Estimation]
    Scale --> API[API Design]
    API --> Data[Data Model]
    Data --> Arch[Architecture]
    Arch --> Deep[Deep Dives]
    Deep --> Trade[Tradeoffs]
```
*Figure: System design interview methodology — structured progression.*


## Chapters

| Chapter | Focus |
|---------|-------|
| System Design Methodology | [System Design Methodology](/docs/system-design/system-design-methodology) |
| URL Shortener | [URL Shortener](/docs/system-design/url-shortener) |
| Distributed Rate Limiter | [Distributed Rate Limiter](/docs/system-design/distributed-rate-limiter) |
| Notification Platform | [Notification Platform](/docs/system-design/notification-platform) |
| Chat Platform | [Chat Platform](/docs/system-design/chat-platform) |
| News Feed | [News Feed](/docs/system-design/news-feed) |
| Distributed Cache Design | [Distributed Cache Design](/docs/system-design/distributed-cache-design) |
| Payment Platform | [Payment Platform](/docs/system-design/payment-platform) |
| Video Streaming Platform | [Video Streaming Platform](/docs/system-design/video-streaming-platform) |
| Search Autocomplete | [Search Autocomplete](/docs/system-design/search-autocomplete) |
| File Storage System | [File Storage System](/docs/system-design/file-storage-system) |
| Dropbox Design | [Dropbox Design](/docs/system-design/dropbox-design) |
| Global Object Store | [Global Object Store](/docs/system-design/global-object-store) |
| Ride Sharing Platform | [Ride Sharing Platform](/docs/system-design/ride-sharing-platform) |
| Global File Transfer Platform | [Global File Transfer Platform](/docs/system-design/global-file-transfer-platform) |
| Metrics Platform | [Metrics Platform](/docs/system-design/metrics-platform) |
| Logging Platform | [Logging Platform](/docs/system-design/logging-platform) |
| Workflow Engine | [Workflow Engine](/docs/system-design/workflow-engine) |
| Kafka-like Event Platform | [Kafka-like Event Platform](/docs/system-design/kafka-like-event-platform) |
| Feature Flag Platform | [Feature Flag Platform](/docs/system-design/feature-flag-platform) |
| API Platform | [API Platform](/docs/system-design/api-platform) |
| Identity Platform | [Identity Platform](/docs/system-design/identity-platform) |
| Secrets Management Platform | [Secrets Management Platform](/docs/system-design/secrets-management-platform) |
| LLM Gateway | [LLM Gateway](/docs/system-design/llm-gateway) |
| Agentic AI Platform Design | [Agentic AI Platform Design](/docs/system-design/agentic-ai-platform-design) |

## Learning Path

1. Start with **System Design Methodology** for the principal-level interview framework.
2. Practice classic exercises: URL shortener, rate limiter, notification platform, chat, and news feed.
3. Progress to storage and media: file storage, Dropbox, object store, video streaming, and search.
4. Study platform designs: metrics, logging, workflow, event bus, feature flags, API, identity, and secrets.
5. Finish with AI-era designs: LLM gateway and agentic AI platform.

## Interview Prep

| Resource | Topic |
|----------|-------|
| [Airbnb Rate Limiting](/docs/real-world-scenarios/airbnb-distributed-rate-limiting) | Global API quotas |
| [Dropbox Sync Conflicts](/docs/real-world-scenarios/dropbox-file-sync-conflicts) | Conflict resolution |
| [Lab 001 consistent hashing](/docs/caching/distributed-caching#25-hands-on-exercise) | Sharding ring on `:8096` |
| [Lab 011 rate limiter](/docs/system-design/distributed-rate-limiter#25-hands-on-exercise) | Token bucket on `:8101` |

## Related Domains

- [Distributed Systems Foundations](/docs/distributed-systems-foundations/overview)
- [Mock Interviews](/docs/mock-interviews/overview)

Return to the [Curriculum Overview](/docs/start-here/curriculum-overview) to see how this domain fits the learning path.
