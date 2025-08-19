# K-map: Biology Data Portal MVP Project Proposal

## 1. Project Overview

**K-map** is a full-stack web project to develop a Minimum Viable Product (MVP) based on React.js and FastAPI, benchmarking the core functionalities of major biology data portals like HuBMAP and GTEx.

The core objective of this project is to enhance accessibility to complex biological data, provide **unique proprietary data from the Korean human body**, and deliver an optimized data visualization experience.

* **Project Duration**: August 14, 2024 – September 11, 2024 (4 weeks total)
* **Target Audience**: Bioinformatics researchers, medical professionals, and students in related fields.
* **Success Metrics**:
    * All planned features are fully functional and successfully deployed within the 4-week period.
    * Receive positive usability feedback from the target users after demos and testing.

---

## 2. Tech Stack

* **Frontend**: React.js, Plotly.js
* **Backend**: Python, FastAPI
* **Database**: PostgreSQL
* **Infra**: Docker

---

## 3. Functional Requirements

### 3.1. User Features

#### **Dataset Page**
This is the core page where users can explore data and view detailed information.

* **List View**
    * **Data Table**: Displays a list with the following columns: `Dataset ID`, `Group`, `Data Type`, `Organ`, `Status`, `Publication Date`.
    * **Filtering and Search**: Supports data filtering based on each column header and keyword-based search functionality.
    * **API**: `GET /datasets`

* **Detail View**
    * Clicking on a specific dataset in the list navigates to its detail page.
    * **Information Provided**: Offers a dataset summary (description, research group, etc.), a table for downloading individual files, citation information, and detailed technical metadata in a key-value table format.
    * **API**: `GET /datasets/{dataset_id}`, `GET /datasets/{dataset_id}/download/{file_name}`

#### **Data Visualization Page**
A page for visually exploring data and gaining insights, built on Plotly.js.

* **Visualization Types & Development Priority**:
    * **1st Priority**: **UMAP Scatter Plot**: Visualizes the distribution of cell types in a 2D space.
    * **2nd Priority**: **Clustered Heatmap**: Groups and displays expression patterns between genes and tissues.
    * **Lower Priority**: Composite visualizations (Boxplot, Pie chart, etc.), Gene Expression Boxplot by tissue.
* **API**: The backend will generate the necessary JSON object to render Plotly charts and deliver it via the `GET /visualizations/{chart_type}` API.

### 3.2. Admin Features

Data management functions accessible only after admin login.

* **Admin Authentication**: Implements a login feature for administrator accounts.
    * **API**: `POST /admin/login`

* **Data Management (CRUD)**: Provides functionality to create (upload), update, and delete datasets and their metadata.
    * **Supported File Formats**: `.csv`, `.json`, `.h5ad`.
    * **Upload/Edit Form**:
        * **Primary Metadata**: Input fields for Dataset ID, Data Type, Organ, Description, etc., using text inputs and dropdowns.
        * **Detailed Technical Metadata**: A feature to dynamically add key-value pairs via an 'Add Field' button.
    * **API**: `POST /admin/datasets` (Create), `PUT /admin/datasets/{dataset_id}` (Update), `DELETE /admin/datasets/{dataset_id}` (Delete).

---

## 4. Development Methodology & Workflow

### 4.1. Core Principles

* **Agile**: Develop incrementally through 1-week sprints for planning, execution, and review.
* **Documentation**: All planning, design, and meeting notes will be recorded and managed in NotebookLM.
* **AI Utilization**: Actively use the Gemini CLI to enhance development productivity in areas like code generation and debugging.

### 4.2. Development Workflow

* **Branching Strategy**: Adopts **Trunk-based Development**, keeping the `main` branch in a deployable state at all times. All feature development occurs in short-lived feature branches.
* **Code Review**: All merges into the `main` branch must go through a **Pull Request (PR)** and be reviewed by at least one other team member.
* **CI (Continuous Integration)**: Utilizes GitHub Actions to automate coding convention checks (ESLint, Ruff) upon PR creation. Branch protection rules will be set to enforce that merges to `main` can only occur after CI passes and a review is approved.

---

## 5. Development Milestones (Weekly Plan)

* **Week 1 (Aug 14 – Aug 21): Core Design & Foundational Scaffolding**
    * **Main Objective**: Complete core frontend/backend design documents (wireframes, API specifications) and implement the basic project structure and codebase for initial integration.

* **Week 2 (Aug 22 – Aug 28): Dataset Page Feature Completion & Visualization Prep**
    * **Main Objective**: Finalize all features for the dataset page (view/download) and complete the technical preparation for the visualization features, including Plotly library integration and basic logic.

* **Week 3 (Aug 29 – Sep 4): Data Visualization & Admin Page Implementation**
    * **Main Objective**: Launch data visualization features (e.g., UMAP) for users and implement the upload and edit functionalities for the admin page.

* **Week 4 (Sep 5 – Sep 11): Final Feature Implementation, Testing & Stabilization**
    * **Main Objective**: Complete all remaining features, including the admin delete function. Conduct comprehensive integration testing based on user scenarios to fix bugs and enhance application stability for the final project wrap-up.

---

## 6. Out of Scope for MVP

The following features will not be included in this 4-week MVP development cycle:

* User registration and login for general users.
* Complex data access permission management based on user groups.
* A separate architecture for the stable processing of large files (tens of GB or more).