import React from "react";

const DatasetsPage = () => {
  // Data from backend/datasets.csv
  const mockupDatasets = [
    {
      id: "HBM264.GZPL.262",
      group: "California Institute of Technology TMC",
      dataType: "sciATACseq [SnapATAC]",
      organ: "Heart",
      status: "Published",
      publicationDate: "2025.08.27"
    },
    {
      id: "HBM788.QPBW.699",
      group: "California Institute of Technology TMC",
      dataType: "sciATACseq",
      organ: "Heart",
      status: "Published",
      publicationDate: "2025.08.27"
    },
    {
      id: "HBM248.QRTB.362",
      group: "TMC - University of Pennsylvania",
      dataType: "H&E Stained Microscopy",
      organ: "Fallopian Tube (Right)",
      status: "Published",
      publicationDate: "2025.08.27"
    },
    {
      id: "HBM453.NSRJ.459",
      group: "TMC - University of Pennsylvania",
      dataType: "H&E Stained Microscopy",
      organ: "Fallopian Tube (Right)",
      status: "Published",
      publicationDate: "2025.08.27"
    },
    {
      id: "HBM984.VGWQ.975",
      group: "TMC - University of Pennsylvania",
      dataType: "H&E Stained Microscopy",
      organ: "Fallopian Tube (Right)",
      status: "Published",
      publicationDate: "2025.08.27"
    },
    {
      id: "HBM756.TGMQ.722",
      group: "TMC - University of Pennsylvania",
      dataType: "H&E Stained Microscopy",
      organ: "Fallopian Tube (Right)",
      status: "Published",
      publicationDate: "2025.08.27"
    },
    {
      id: "HBM826.BQLS.392",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM487.WQJK.386",
      group: "University of California San Diego TMC",
      dataType: "snATACseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM247.JXLL.982",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM563.PSVZ.888",
      group: "University of California San Diego TMC",
      dataType: "snATACseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM396.MBBD.429",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM237.LCJZ.985",
      group: "University of California San Diego TMC",
      dataType: "snATACseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM358.CJQN.957",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM787.NMMD.653",
      group: "University of California San Diego TMC",
      dataType: "snATACseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM352.WMTT.589",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM622.QNZX.878",
      group: "University of California San Diego TMC",
      dataType: "snATACseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM773.GNCH.235",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM554.PNZB.945",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM665.DPXD.498",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    },
    {
      id: "HBM683.VVMH.842",
      group: "University of California San Diego TMC",
      dataType: "snRNAseq (SNARE-seq2)",
      organ: "Lung (Right)",
      status: "Published",
      publicationDate: "2025.08.24"
    }
  ];

  // Get organ tag color - Figma 정확한 색상
  const getOrganTagColor = (organ) => {
    const organColors = {
      'Blood': '#c45353',
      'Heart': '#c45353', 
      'Bronchus': '#cf933e',
      'Lung': '#cf933e',
      'Lung (Right)': '#cf933e',
      'Lung (Left)': '#cf933e',
      'Stomach': '#39acd7',
      'Brain': '#39acd7',
      'Small Intestine': '#39acd7',
      'Large Intestine': '#39acd7',
      'Bone': '#7b1fa2',
      'Knee': '#7b1fa2',
      'Fallopian Tube (Right)': '#d1548e',
      'Fallopian Tube (Left)': '#d1548e',
      'Fallopian Tube': '#d1548e'
    };
    return organColors[organ] || '#666';
  };

  const getOrganTagBackground = (organ) => {
    const organBGs = {
      'Blood': '#ffd7d7',
      'Heart': '#ffd7d7',
      'Bronchus': '#ffe3bc', 
      'Lung': '#ffe3bc',
      'Lung (Right)': '#ffe3bc',
      'Lung (Left)': '#ffe3bc',
      'Stomach': '#c5e2ed',
      'Brain': '#c5e2ed',
      'Small Intestine': '#c5e2ed',
      'Large Intestine': '#c5e2ed',
      'Bone': '#d5c5ed',
      'Knee': '#d5c5ed',
      'Fallopian Tube (Right)': '#ffd0e3',
      'Fallopian Tube (Left)': '#ffd0e3',
      'Fallopian Tube': '#ffd0e3'
    };
    return organBGs[organ] || '#f0f0f0';
  };

  return (
    <div className="figma-datasets-page">
      {/* Header with navigation */}
      <div className="figma-header">
        <div className="figma-breadcrumb">
          <span className="breadcrumb-item">●</span>
          <span className="breadcrumb-item">K-MAP</span>
          <span className="breadcrumb-separator">›</span>
          <span className="breadcrumb-item current">Datasets</span>
        </div>
      </div>

      <div className="figma-main-container">
        {/* Left Sidebar - Figma 정확한 디자인 */}
        <aside className="figma-sidebar">
          {/* Sidebar Header */}
          <div className="sidebar-header-section">
            <div className="sidebar-logo">
              <span className="logo-icon"></span>
              <span className="logo-text">K-MAP</span>
              <span className="breadcrumb-arrow">›</span>
              <span className="current-page">Datasets</span>
            </div>
          </div>

          {/* Search Bar */}
          <div className="sidebar-search">
            <input
              type="text"
              placeholder="Search Filters..."
              className="sidebar-search-input"
            />
            <span className="search-icon"></span>
          </div>

          {/* Static Filter Sections */}
          <div className="filter-sections">
            {/* Dataset ID */}
            <div className="filter-section">
              <div className="filter-section-header">
                <div className="filter-header-content">
                  <span className="filter-icon"></span>
                  <span className="filter-title">Dataset ID</span>
                </div>
                <span className="filter-toggle">
                  <svg width="10" height="6" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1L5 5L9 1" stroke="#9a9a9a" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </span>
              </div>
            </div>

            {/* Group */}
            <div className="filter-section">
              <div className="filter-section-header">
                <div className="filter-header-content">
                  <span className="filter-icon"></span>
                  <span className="filter-title">Group</span>
                </div>
                <span className="filter-toggle">
                  <svg width="10" height="6" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1L5 5L9 1" stroke="#9a9a9a" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </span>
              </div>
            </div>

            {/* Data Type */}
            <div className="filter-section">
              <div className="filter-section-header">
                <div className="filter-header-content">
                  <span className="filter-icon"></span>
                  <span className="filter-title">Data Type</span>
                </div>
                <span className="filter-toggle">
                  <svg width="10" height="6" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1L5 5L9 1" stroke="#9a9a9a" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </span>
              </div>
            </div>

            {/* Organ - Expanded state showing static data */}
            <div className="filter-section organ-section">
              <div className="filter-section-header active">
                <div className="filter-header-content">
                  <span className="filter-icon active"></span>
                  <span className="filter-title active">Organ</span>
                </div>
                <span className="filter-toggle expanded">
                  <svg width="10" height="6" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1L5 5L9 1" stroke="#9a9a9a" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </span>
              </div>
              <div className="filter-section-content expanded">
                {/* Static organ list with Figma exact data */}
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-blood"></span>
                    <span className="organ-name">Blood</span>
                  </div>
                  <span className="organ-count">3</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-heart"></span>
                    <span className="organ-name">Heart</span>
                  </div>
                  <span className="organ-count">14</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-bronchus"></span>
                    <span className="organ-name">Bronchus</span>
                  </div>
                  <span className="organ-count">1</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-lung"></span>
                    <span className="organ-name">Lung</span>
                  </div>
                  <span className="organ-count">59</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-brain"></span>
                    <span className="organ-name">Brain</span>
                  </div>
                  <span className="organ-count">265</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-stomach"></span>
                    <span className="organ-name">Stomach</span>
                  </div>
                  <span className="organ-count">3</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-small-intestine"></span>
                    <span className="organ-name">Small Intestine</span>
                  </div>
                  <span className="organ-count">53</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-large-intestine"></span>
                    <span className="organ-name">Large Intestine</span>
                  </div>
                  <span className="organ-count">58</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-bone"></span>
                    <span className="organ-name">Bone</span>
                  </div>
                  <span className="organ-count">9</span>
                </div>
                <div className="organ-item">
                  <div className="organ-item-left">
                    <span className="organ-color-dot organ-knee"></span>
                    <span className="organ-name">Knee</span>
                  </div>
                  <span className="organ-count">79</span>
                </div>
              </div>
            </div>

            {/* Status */}
            <div className="filter-section">
              <div className="filter-section-header">
                <div className="filter-header-content">
                  <span className="filter-icon"></span>
                  <span className="filter-title">Status</span>
                </div>
                <span className="filter-toggle">
                  <svg width="10" height="6" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1L5 5L9 1" stroke="#9a9a9a" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </span>
              </div>
            </div>

            {/* Publication Date */}
            <div className="filter-section">
              <div className="filter-section-header no-border">
                <div className="filter-header-content">
                  <span className="filter-icon"></span>
                  <span className="filter-title">Publication Date</span>
                </div>
                <span className="filter-toggle">
                  <svg width="10" height="6" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1L5 5L9 1" stroke="#9a9a9a" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </span>
              </div>
            </div>
          </div>

          {/* Bottom Actions */}
          <div className="sidebar-bottom">
            <div className="sidebar-bottom-left">
              <button className="sidebar-icon">
                <span></span>
              </button>
            </div>
            <div className="sidebar-bottom-right">
              <button className="sidebar-icon">
                <span></span>
              </button>
              <button className="sidebar-icon">
                <span></span>
              </button>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="figma-content">
          {/* Active Filter Tags and Clear Button - Figma Exact Design */}
          <div className="figma-filters-bar">
            <div className="active-filter-tags">
              {/* Blood Filter - Active */}
              <span className="active-filter-tag filter-blood">
                <span className="filter-icon-small"></span>
                Blood
                <button className="remove-filter-btn">×</button>
              </span>
              
              {/* Heart Filter - Active */}
              <span className="active-filter-tag filter-heart">
                <span className="filter-icon-small"></span>
                Heart
                <button className="remove-filter-btn">×</button>
              </span>
              
              {/* Bronchus Filter - Active */}
              <span className="active-filter-tag filter-bronchus">
                <span className="filter-icon-small"></span>
                Bronchus
                <button className="remove-filter-btn">×</button>
              </span>
              
              {/* Stomach Filter - Crossed out (inactive) */}
              <span className="active-filter-tag filter-stomach crossed-out">
                <span className="filter-icon-small"></span>
                Stomach
                <button className="remove-filter-btn">×</button>
              </span>
              
              {/* Large Intestine Filter - Crossed out (inactive) */}
              <span className="active-filter-tag filter-large-intestine crossed-out">
                <span className="filter-icon-small"></span>
                Large Intestine
                <button className="remove-filter-btn">×</button>
              </span>
            </div>
            <div className="clear-filters-btn">
              Clear Filters
            </div>
          </div>

          {/* Results Count and Table */}
          <div className="figma-table-container">
            {/* Data Table with Static Mockup Data */}
            <table className="figma-table">
              <thead>
                <tr>
                  {/* Dataset ID - Sorted (active) */}
                  <th className="table-header-cell sortable sorted">
                    <span className="sort-icon"></span>
                    Dataset ID
                  </th>
                  {/* Group - Sortable */}
                  <th className="table-header-cell sortable">
                    <span className="sort-icon"></span>
                    Group
                  </th>
                  {/* Data Type - Sortable */}
                  <th className="table-header-cell sortable">
                    <span className="sort-icon"></span>
                    Data Type
                  </th>
                  {/* Organ - Sortable */}
                  <th className="table-header-cell sortable">
                    <span className="sort-icon"></span>
                    Organ
                  </th>
                  {/* Status - Sortable */}
                  <th className="table-header-cell sortable">
                    <span className="sort-icon"></span>
                    Status
                  </th>
                  {/* Publication Date - Sortable */}
                  <th className="table-header-cell sortable">
                    <span className="sort-icon"></span>
                    Publication Date
                  </th>
                </tr>
              </thead>
              <tbody>
                {mockupDatasets.map(dataset => (
                  <tr 
                    key={dataset.id}
                    className="table-row"
                  >
                    <td>
                      <span className="dataset-id">{dataset.id}</span>
                    </td>
                    <td>{dataset.group}</td>
                    <td>{dataset.dataType}</td>
                    <td>
                      <span 
                        className="organ-tag"
                        style={{ 
                          backgroundColor: getOrganTagBackground(dataset.organ),
                          color: getOrganTagColor(dataset.organ),
                          border: `1px solid ${getOrganTagColor(dataset.organ)}`
                        }}
                      >
                        {dataset.organ}
                      </span>
                    </td>
                    <td>
                      <span className="status-badge">
                        {dataset.status}
                      </span>
                    </td>
                    <td>{dataset.publicationDate}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </div>
  );
};

export default DatasetsPage;