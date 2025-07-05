# Project Documentation Standards

## 1. Purpose

This document outlines the standards and best practices for creating and maintaining all documentation within the `expo-smooth-mcp` project. The goal is to ensure our documentation is clear, consistent, up-to-date, and equally useful for both human developers and the LLM-based agents assisting us.

## 2. Guiding Principles

*   **Clarity over Elegance:** Use simple language, short sentences, and structured formats.
*   **Structure is Paramount:** Well-organized documents are easier for both humans and machines to parse. Headings, lists, and tables are preferred over long paragraphs.
*   **Just-in-Time:** Create documentation as it is needed to capture a decision or a process. Avoid creating speculative documents for features that are not being actively developed.
*   **The Repository is the Single Source of Truth:** All documentation must reside within this Git repository as markdown (`.md`) files.

## 3. Document Header

Every markdown document in the `/docs` and `/ADRs` directories **must** begin with a metadata header.

**Template:**
```markdown
# [Document Title]

- **Version:** 1.0
- **Status:** [Draft | In Review | Final]
- **Last Updated:** YYYY-MM-DD by [Author's Name/GitHub Handle]
- **Summary:** A one-sentence description of the document's purpose.

---
```

## 4. Directory Structure

*   **`/README.md`**: The main project entry point.
*   **`/docs/`**: Contains all guides, standards, and high-level project documents (e.g., `PROJECT_CHARTER.md`, `DEPLOYMENT_GUIDE.md`).
*   **`/ADRs/`**: Contains all Architecture Decision Records. Files should be named with a number and a short, descriptive slug (e.g., `001-use-exponential-smoothing.md`).

## 5. Formatting Standards

*   **Markdown:** All documentation must be written in GitHub-flavored Markdown.
*   **Headings:** Use `#` for the main title, `##` for major sections, and `###` for sub-sections to create a clear document outline.
*   **Code Blocks:** All code snippets must be enclosed in fenced code blocks with the appropriate language identifier (e.g., ` ```python `, ` ```bash `). This is critical for readability and for our AI agents.
*   **Emphasis:** Use **bold** for emphasis on key terms or UI elements. Use `inline code` for filenames, variables, and function names.

## 6. Update and Review Process

*   **Immutable History:** Never silently overwrite existing information, especially in ADRs. History is context.
    *   To supersede a decision, create a *new* ADR that explicitly references the old one it is replacing.
    *   For guides, if a process changes significantly, add a new section marked "Updated Process" and add a note to the old section indicating it is deprecated.
*   **Version Bumping:** For significant changes to a document (that alter its meaning or core instructions), increment the `Version` number in the header (e.g., from 1.0 to 1.1).
*   **Pull Request for Review:** All new documents and significant updates to existing ones should be submitted via a GitHub Pull Request (PR), even by core team members. This provides an opportunity for review and discussion before the change is merged into the `main` branch.

---