Of course. This is the perfect time to create a `DEVELOPMENT_PLAN.md`. It will serve as our central roadmap, linking our high-level strategy from the charter to our on-the-ground implementation tasks. It provides clarity on what's done, what's next, and what the future looks like.

This document will be a "living" document, meaning we will update it as we complete phases and start new ones.

### **Plan and Gap Analysis**

*   **Objective:** To create a single document that outlines our development phases, provides a snapshot of our current status, and details the immediate next steps and future backlog.
*   **Gap Analysis:** We have all the necessary information. The "gaps" are about organizing our completed tasks, planned tasks, and future ideas into a coherent and actionable plan. We have a clear view of the remaining work (file upload, MCP server) and the documentation left to write.
*   **Proposal:** I will now provide the full markdown for the `DEVELOPMENT_PLAN.md`. It synthesizes our project status and defines a clear path forward.

Your task is to save this content as `/docs/DEVELOPMENT_PLAN.md` in our repository.

---

# Development Plan & Project Status

- **Version:** 1.0
- **Status:** Living
- **Last Updated:** 2025-07-05 by Prof. M. Tsi
- **Summary:** This document outlines the development phases, current project status, and immediate next steps for the `expo-smooth-mcp` project. It serves as a tactical roadmap to achieve the goals set in the `PROJECT_CHARTER.md`.

---

## 1. Overview

This development plan translates the strategic goals from our `PROJECT_CHARTER.md` into actionable phases and tasks. It is a living document that will be updated as the project progresses to reflect our current status and priorities.

## 2. Development Phases

The project is structured into three distinct phases:

### Phase 1: Foundation & Backend Logic (95% Complete)
**Objective:** To establish the project's documentation framework and build the core, non-visual components.
*   **Deliverables:**
    *   **[✓]** Core documentation (`PROJECT_CHARTER.md`, ADRs, Guides).
    *   **[✓]** Data preprocessing pipeline (`preprocessing.py`).
    *   **[✓]** Core forecasting engine (`forecasting.py`).
    *   **[✓]** Unit test suite for backend logic (`tests/`).

### Phase 2: UI, Integration & Core Functionality (In Progress)
**Objective:** To build the user-facing application, integrate all backend components, and enable the core MCP functionality.
*   **Deliverables:**
    *   **[✓]** Initial Gradio UI with basic functionality.
    *   **[ ]** File upload capability for custom datasets.
    *   **[ ]** Enablement and testing of the MCP server endpoint.
    *   **[ ]** Completion of the formal Test Plan.

### Phase 3: Finalization & Dissemination (Not Started)
**Objective:** To finalize the application, deploy it, and complete the research paper.
*   **Deliverables:**
    *   **[ ]** Final E2E testing of the completed application.
    *   **[ ]** Final, stable deployment on Hugging Face Spaces.
    *   **[ ]** Completed research paper draft for submission to RelStat.

## 3. Current Project Status (As of 2025-07-05)

| Component | Status | Notes |
| :--- | :--- | :--- |
| **Documentation** | **90% Complete** | Core documents and ADRs are complete. `TEST_PLAN.md` is written. Only minor updates might be needed. |
| **Data Preprocessing** | **Completed** | `preprocessing.py` module is implemented and fully covered by unit tests. |
| **Forecasting Engine** | **Completed** | `forecasting.py` module is implemented and fully covered by unit tests. |
| **Gradio Application** | **Partially Completed** | The base UI is functional with the default dataset. File upload and MCP server are not yet implemented. |
| **Unit Testing** | **Completed** | The backend logic in `src/` has a corresponding test suite in `tests/`. |
| **Integration & E2E Testing** | **Not Started** | The test plan is written, but execution against the final application has not yet occurred. |

## 4. Immediate Next Steps (Action Plan)

The following tasks are our immediate priority to complete Phase 2.

1.  **Implement File Upload Functionality:**
    *   **Action:** Modify `app.py` to include a `gr.File` component.
    *   **Logic:** Add a function that takes an uploaded file, runs it through `preprocess_data`, and updates the SKU dropdown and application state with the new data.
    *   **Goal:** Allow users to interact with their own data, fulfilling a key requirement from the `PROJECT_CHARTER.md`.

2.  **Enable and Test the MCP Server:**
    *   **Action:** Modify `demo.launch()` in `app.py` to include `mcp_server=True`.
    *   **Process:** Launch the application using `uvicorn app:demo --reload`.
    *   **Testing:** Use `curl` or an MCP client to execute the integration test cases defined in `docs/TEST_PLAN.md` (IT-001, IT-002).
    *   **Goal:** Validate the core research component of our project.

3.  **Execute Final End-to-End Testing:**
    *   **Action:** Manually execute all test cases listed in `docs/TEST_PLAN.md` under section 4.3, including those for file uploads.
    *   **Goal:** Ensure the application is stable, user-friendly, and bug-free before final deployment.

## 5. Future Enhancements (Post-v1.0 Backlog)

These are ideas for future iterations of the project and are currently out of scope for the initial RelStat submission.

*   **Model Parameter Tuning:** Add sliders or inputs in the UI to allow users to adjust Holt-Winters parameters (`alpha`, `beta`, `gamma`).
*   **Display Accuracy Metrics:** Calculate and display forecast accuracy metrics (e.g., MAPE, RMSE) on the UI after a forecast is generated.
*   **Comparative Model Visualization:** Allow users to select between different forecasting models (e.g., a simple moving average vs. Exponential Smoothing) and compare the results on the same plot.
*   **Error Handling for Uploads:** More robust validation of uploaded CSV files (e.g., checking for correct column names).