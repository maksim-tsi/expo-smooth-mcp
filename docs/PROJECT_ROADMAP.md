# Expo Smooth MCP - Project Roadmap

**Last Updated:** 2025-10-13  
**Project Status:** 📋 Specification Complete - Ready for Implementation  
**Version:** 2.0

---

## Quick Status Overview

| Phase | Tasks | Est. Hours | Status | Progress |
|-------|-------|------------|--------|----------|
| **Phase 1:** Decouple Logic | 8 | 12h | ✅ Complete | 100% |
| **Phase 2:** FastMCP Backend | 12 | 20h | ✅ Complete | 100% |
| **Phase 3:** Mount Gradio | 6 | 8h | ✅ Complete | 100% |
| **Phase 3A:** Custom Data Support | 4 | 7h | ✅ Complete | 100% |
| **Phase 3B:** Column Mapping | 6 | 9.5h | ⏸️ Ready | 0% |
| **Phase 4:** Deployment | 8 | 9h | ⏸️ Ready | 0% |
| **Phase 5:** Production | 14 | 22h | ⏸️ Ready | 0% |
| **Phase 6:** Documentation | 10 | 16h | ⏸️ Ready | 0% |
| **TOTAL** | **68** | **103.5h** | - | **54%** |

---

## Project Timeline

### Current Sprint
**🎯 Next Up:** Phase 3B - Intelligent Column Mapping

### Completed Milestones
- ✅ **2025-10-10:** Phase 1 specification complete
- ✅ **2025-10-11:** Phases 2-5 specification complete
- ✅ **2025-10-13:** Phase 6 specification complete
- ✅ **2025-10-13:** Documentation restructure complete
- ✅ **2025-10-13:** Phase 1 implementation complete (logic decoupled)
- ✅ **2025-10-13:** Phase 2 implementation complete (FastMCP + FastAPI)
- ✅ **2025-10-13:** Phase 3 implementation complete (Gradio UI mounted)
- ✅ **2025-10-13:** Phase 3 code review complete (bug fixed)
- ✅ **2025-10-13:** Phase 4 documentation complete (deployment guides)
- ✅ **2025-10-13:** ADR 005 created (custom data support)
- ✅ **2025-10-13:** Phase 3A specification complete
- ✅ **2025-10-13:** Phase 3A implementation complete (custom data support)
- ✅ **2025-10-13:** Phase 3A code review complete (17 tests, all passing)
- ✅ **2025-10-13:** ADR 005 extended (flexible column mapping)
- ✅ **2025-10-13:** Phase 3B specification complete (column mapping)

### Upcoming Milestones
- ⏳ **TBD:** Phase 3B implementation complete (intelligent column mapping)
- ⏳ **TBD:** Phase 4 implementation complete (Docker MCP + Fly.io)
- ⏳ **TBD:** Phase 5 implementation complete (production-ready)
- ⏳ **TBD:** Phase 6 implementation complete (fully documented)
- ⏳ **TBD:** 🎉 Project complete & production deployed

---

## Phase Details

### Phase 1: Decouple Business Logic ✅
**Duration:** ~12 hours (8 tasks)  
**Status:** Specification complete, ready for implementation  
**Dependencies:** None

**Objective:** Extract business logic from UI layer into framework-agnostic module.

**Key Deliverables:**
- `src/expo_smooth_mcp/logic.py` with 5 core functions
- Refactored `app.py` delegating to logic module
- Unit test suite with >90% coverage

**Implementation Guide:** [Phase 1 Implementation](implementation/PHASE_1_IMPLEMENTATION.md)

---

### Phase 2: FastMCP Backend ⏸️
**Duration:** ~20 hours (12 tasks)  
**Status:** Specification complete, not started  
**Dependencies:** Phase 1 complete

**Objective:** Build production-grade MCP server with dual transport support.

**Key Deliverables:**
- FastMCP server with stdio + HTTP/SSE transports
- 3 MCP tools (generate_forecast, list_products, get_product_history)
- JWT authentication
- REST API endpoints
- Comprehensive test suite

**Key Features:**
- ✨ Dual transport (stdio for local, HTTP/SSE for remote)
- 🔐 JWT-based authentication
- 📊 Prometheus metrics
- 🧪 >90% test coverage

**Tasks:**
- TASK-201 through TASK-212
- Install dependencies → Configure server → Implement tools → Add auth → Testing

**Implementation Guide:** [Phase 2 Implementation](implementation/PHASE_2_IMPLEMENTATION.md) *(to be created)*

---

### Phase 3: Mount Gradio UI ⏸️
**Duration:** ~8 hours (6 tasks)  
**Status:** Specification complete, not started  
**Dependencies:** Phase 2 complete

**Objective:** Integrate existing Gradio app as sub-application within FastAPI.

**Key Deliverables:**
- Gradio mounted at `/gradio` route
- Backward-compatible UI
- Authentication integration
- Updated navigation

**Key Features:**
- 🎨 Existing UI preserved
- 🔗 Seamless integration with FastAPI
- 🔐 Optional authentication
- 📱 Responsive design maintained

**Tasks:**
- TASK-301 through TASK-306
- Mount Gradio → Update paths → Add auth → Cross-link → Testing

**Implementation Guide:** [Phase 3 Implementation](implementation/PHASE_3_IMPLEMENTATION.md) *(to be created)*

---

### Phase 3B: Intelligent Column Mapping ⏸️
**Duration:** ~9.5 hours (6 tasks)  
**Status:** Specification complete, ready for implementation  
**Dependencies:** Phase 3A complete

**Objective:** Enable automatic column detection and flexible mapping to work with diverse data formats commonly found in supply chain management.

**Key Deliverables:**
- Lightweight column analysis module with heuristic detection
- Interactive column mapping UI in Gradio
- Extended MCP tool with column mapping parameters
- Refactored backend for column flexibility
- Comprehensive test suite (15+ tests)
- Updated documentation

**Key Features:**
- 🔍 Automatic column type detection (date, metric, product)
- 🎯 Smart suggestions based on common SCM naming patterns
- 🎨 Interactive dropdowns for manual column selection
- 🔧 MCP tool accepts custom column names
- ⚡ Lightweight heuristics (<100ms analysis)
- ✅ >80% accuracy on standard SCM datasets
- 🔄 Backward compatible with existing data

**Column Detection:**
- **Date columns:** `date`, `timestamp`, `order_date`, `period`, `ds`, etc.
- **Metric columns:** `sales`, `quantity`, `demand`, `revenue`, `units_sold`, etc.
- **Product columns:** `sku`, `product_id`, `item_id`, `product_code`, etc.

**Tasks:**
- TASK-3B-01: Create column analysis module (2h)
- TASK-3B-02: Update Gradio UI with mapping interface (2h)
- TASK-3B-03: Extend MCP tool with column parameters (1.5h)
- TASK-3B-04: Refactor backend for flexibility (1.5h)
- TASK-3B-05: Create comprehensive test suite (1.5h)
- TASK-3B-06: Update documentation (1h)

**Implementation Guide:** [Phase 3B Implementation](implementation/PHASE_3B_IMPLEMENTATION.md)  
**Quick Start:** [Phase 3B Quick Start](implementation/PHASE_3B_QUICKSTART.md)  
**Architecture Decision:** [ADR 005 Extension](../ADRs/005-support-user-provided-data.md)

---

### Phase 4A: Docker MCP Toolkit Deployment ⏸️
**Duration:** ~10 hours (7 tasks)  
**Status:** Specification complete, not started  
**Dependencies:** Phase 3 complete

**Objective:** Enable local deployment using Docker MCP Toolkit for Claude Desktop integration.

**Key Deliverables:**
- Dockerfile optimized for stdio transport
- Docker MCP Toolkit configuration
- Claude Desktop integration
- Local testing documentation

**Key Features:**
- 🐳 Docker MCP Toolkit support
- 💻 Claude Desktop stdio integration
- ⚡ Fast local performance
- 🆓 Free to run

**Tasks:**
- TASK-401 through TASK-407
- Create Dockerfile → Configure toolkit → Test stdio → Document integration

**Implementation Guide:** [Phase 4A Implementation](implementation/PHASE_4A_IMPLEMENTATION.md) *(to be created)*

---

### Phase 4B: Fly.io Cloud Deployment ⏸️
**Duration:** ~12 hours (8 tasks)  
**Status:** Specification complete, not started  
**Dependencies:** Phase 4A complete

**Objective:** Enable cloud deployment to Fly.io for public HTTP/SSE access.

**Key Deliverables:**
- Fly.io configuration (fly.toml)
- Production Dockerfile
- Redis integration
- Health checks and monitoring
- Deployment documentation

**Key Features:**
- ☁️ Cloud-hosted MCP server
- 🌐 HTTP/SSE transport for remote access
- 📈 Auto-scaling
- 🔒 Production-grade security

**Tasks:**
- TASK-408 through TASK-415
- Create fly.toml → Configure Redis → Deploy → Setup monitoring → Document

**Implementation Guide:** [Phase 4B Implementation](implementation/PHASE_4B_IMPLEMENTATION.md) *(to be created)*

---

### Phase 5: Production Hardening ⏸️
**Duration:** ~22 hours (14 tasks)  
**Status:** Specification complete, not started  
**Dependencies:** Phase 4B complete

**Objective:** Add enterprise-grade features for production readiness.

**Key Deliverables:**
- Enhanced JWT authentication with scopes
- Redis-based rate limiting
- Structured logging (JSON format)
- Prometheus metrics
- Security hardening
- Performance optimization
- Comprehensive test coverage

**Key Features:**
- 🔐 Multi-tier authentication (user/admin scopes)
- 🚦 Rate limiting per endpoint
- 📊 Full observability (logs + metrics)
- 🔒 Security best practices
- ⚡ Performance optimization
- 🧪 E2E testing

**Tasks:**
- TASK-501 through TASK-514
- 14 tasks covering auth, rate limiting, logging, metrics, security, testing

**Implementation Guide:** [Phase 5 Implementation](implementation/PHASE_5_IMPLEMENTATION.md) *(to be created)*

---

### Phase 6: Documentation & Testing ⏸️
**Duration:** ~16 hours (10 tasks)  
**Status:** Specification complete, not started  
**Dependencies:** Phase 5 complete

**Objective:** Complete comprehensive documentation and validation testing.

**Key Deliverables:**
- Updated README with architecture
- Complete deployment guides
- Client integration guides (Claude Desktop, Cursor, VS Code)
- API documentation
- Troubleshooting guide
- Performance benchmarks
- Load testing suite
- Updated ADRs
- E2E testing checklist

**Key Features:**
- 📚 Complete documentation set
- 🔧 Troubleshooting guides
- 📊 Performance benchmarks
- 🧪 Load testing framework
- ✅ E2E validation

**Tasks:**
- TASK-601 through TASK-610
- Documentation updates → Benchmarking → Load testing → Final validation

**Implementation Guide:** [Phase 6 Implementation](implementation/PHASE_6_IMPLEMENTATION.md) *(to be created)*

---

## Resource Planning

### Solo Developer Timeline
- **Full-time (8h/day):** ~12-13 working days
- **Part-time (4h/day):** ~25 working days
- **Weekend projects (8h/week):** ~12-13 weeks

### Two-Developer Timeline
**Parallel track assignments:**

**Developer 1 (Backend Focus):**
- Phase 1: All logic decoupling
- Phase 2: FastMCP implementation
- Phase 5: Security & production features

**Developer 2 (Integration Focus):**
- Phase 3: Gradio mounting
- Phase 4: Docker & Fly.io deployment
- Phase 6: Documentation & testing

**Estimated Duration:** 7-10 working days with good coordination

### Three-Developer Timeline
**Highly parallel execution:**

**Developer 1:** Phases 1-2 (backend)  
**Developer 2:** Phases 3-4 (deployment)  
**Developer 3:** Phases 5-6 (production + docs)

**Estimated Duration:** 5-7 working days

---

## Risk Assessment

### Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| FastMCP API changes | Low | Pin version, monitor releases |
| Docker MCP Toolkit issues | Medium | Fallback to stdio testing |
| Fly.io deployment complexity | Low | Well-documented process |
| Rate limiting edge cases | Medium | Comprehensive testing |
| Performance degradation | Low | Continuous benchmarking |

### Project Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Scope creep | Medium | Strict adherence to specification |
| Testing time underestimated | Medium | Buffer time in estimates |
| Documentation gaps | Low | Phase 6 dedicated to docs |
| Integration issues | Medium | Incremental testing |

---

## Success Criteria

### Functional Requirements
- ✅ All 65 tasks completed
- ✅ All acceptance criteria met
- ✅ Both deployments working (Docker + Fly.io)
- ✅ Claude Desktop integration functional
- ✅ All tests passing (unit + integration + E2E)

### Performance Requirements
- ✅ Health check p95 latency <100ms (local), <200ms (prod)
- ✅ Forecast API p95 latency <1000ms (local), <2000ms (prod)
- ✅ Throughput >10 req/s for forecast API
- ✅ Error rate <1%

### Quality Requirements
- ✅ Test coverage >90%
- ✅ Zero critical security vulnerabilities
- ✅ Complete documentation
- ✅ Production monitoring configured

---

## Project Dependencies

### External Dependencies
- FastMCP library (v2.0+)
- FastAPI (v0.104+)
- Docker MCP Toolkit
- Fly.io platform
- Redis (for rate limiting)

### Internal Dependencies
```
Phase 1 → Phase 2 → Phase 3 → Phase 4A → Phase 4B → Phase 5 → Phase 6
                                    ↓
                              (Some tasks can
                               start in parallel)
```

**Parallelization Opportunities:**
- Phase 4A & 4B: Some documentation can be written in parallel
- Phase 5: Auth, rate limiting, logging can be developed in parallel
- Phase 6: Most documentation tasks are independent

---

## Communication Plan

### Status Updates
- **Daily:** Update task status in this roadmap
- **Weekly:** Review progress vs. estimates
- **Phase completion:** Update README and notify stakeholders

### Documentation
- **During development:** Update inline code comments
- **After each task:** Update acceptance criteria checkboxes
- **Phase completion:** Update phase-specific implementation guides

---

## Quick Reference

### Key Documents
- [SPECIFICATION.md](SPECIFICATION.md) - Complete technical specification (21,000+ lines)
- [PROJECT_CHARTER.md](PROJECT_CHARTER.md) - Project goals and requirements
- [Implementation Guides](implementation/) - Phase-specific guides
- [ADRs](../ADRs/) - Architectural decision records

### Useful Commands
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Check linting
pylint src/

# Type checking
mypy src/

# Start local server
python app.py

# Deploy to Fly.io
fly deploy

# Run benchmarks
python scripts/benchmark.py
```

---

## Notes

- All 65 tasks have complete specifications ready for implementation
- Each task is designed for ≤2 hours of work by experienced Python developer
- Comprehensive code examples provided for all major components
- Test-driven development approach recommended
- Incremental deployment strategy reduces risk

---

**Last Review:** 2025-10-13  
**Next Review:** TBD (when Phase 1 implementation begins)  
**Project Owner:** maksim-tsi
