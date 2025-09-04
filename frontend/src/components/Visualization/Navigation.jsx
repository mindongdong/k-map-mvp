import React from 'react';
import './Navigation.css';

const Navigation = ({ selectedOptions }) => {
  const getBreadcrumb = () => {
    if (selectedOptions.tissue) {
      return {
        main: "Multi-Gene Single Cell",
        sub: "Sort by Tissue"
      };
    } else if (selectedOptions.cellType) {
      return {
        main: "Multi-Gene Single Cell",
        sub: "Sort by Cell Type"
      };
    } else if (selectedOptions.umap1) {
      return {
        main: "UMAP",
        sub: "UMAP"
      };
    } else if (selectedOptions.umapFeature) {
      return {
        main: "UMAP",
        sub: "UMAP Feature"
      };
    } else {
      return {
        main: "Multi-Gene Single Cell",
        sub: "Sort by Tissue"
      };
    }
  };

  const breadcrumb = getBreadcrumb();

  return (
    <div className="header">
      <div className="breadcrumb">
        <span className="breadcrumb-item">{breadcrumb.main}</span>
        <span className="breadcrumb-separator">❯</span>
        <span className="breadcrumb-item">{breadcrumb.sub}</span>
      </div>
    </div>
  );
};

export default Navigation;