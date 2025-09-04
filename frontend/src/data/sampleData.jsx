
export const generateTissueData = (geneName = 'PECAM1') => {
  const tissues = ['Brain', 'Heart', 'Liver', 'Lung', 'Kidney', 'Muscle', 'Skin'];
  const cellTypes = ['Neuron', 'Cardiomyocyte', 'Hepatocyte', 'Alveolar', 'Epithelial', 'Myocyte', 'Keratinocyte'];
  
  const groups = [];
  const expressionData = [];
  const cellFractionData = [];
  const totalCellData = [];
  
  tissues.forEach((tissue, tissueIdx) => {
    cellTypes.forEach((cellType, cellTypeIdx) => {
      const group = `${cellType} | ${tissue}`;
      groups.push(group);
      
      // Expression 데이터 (boxplot용) - 실제와 유사한 분포
      const nPoints = 30 + Math.floor(Math.random() * 70);
      const baseExpression = Math.random() * 4;
      const expression = Array.from({ length: nPoints }, () => 
        Math.max(0, baseExpression + (Math.random() - 0.5) * 2.5)
      );
      
      expressionData.push({
        group: group,
        values: expression,
        tissue: tissue,
        celltype: cellType
      });
      
      // Cell fraction (pie chart용) - 0~0.8 범위
      const cellFraction = Math.random() * 0.8;
      cellFractionData.push({
        group: group,
        fraction: cellFraction,
        tissue: tissue,
        celltype: cellType
      });
      
      // Total cell count (dot size용) - 10~150 범위
      const totalCell = 10 + Math.floor(Math.random() * 140);
      totalCellData.push({
        group: group,
        count: totalCell,
        tissue: tissue,
        celltype: cellType
      });
    });
  });
  
  return {
    geneName,
    groups,
    expressionData,
    cellFractionData,
    totalCellData,
    tissues,
    cellTypes
  };
};

// Cell Type으로 정렬된 데이터 (Plot 2용)
export const generateCellTypeData = (geneName = 'PECAM1') => {
  const data = generateTissueData(geneName);
  
  // Cell type으로 정렬
  const sortedData = {
    ...data,
    expressionData: data.expressionData.sort((a, b) => a.celltype.localeCompare(b.celltype)),
    cellFractionData: data.cellFractionData.sort((a, b) => a.celltype.localeCompare(b.celltype)),
    totalCellData: data.totalCellData.sort((a, b) => a.celltype.localeCompare(b.celltype))
  };
  
  // x 좌표 재설정
  sortedData.expressionData.forEach((item, index) => {
    item.x = index;
  });
  sortedData.cellFractionData.forEach((item, index) => {
    item.x = index;
  });
  sortedData.totalCellData.forEach((item, index) => {
    item.x = index;
  });
  
  return sortedData;
};

// UMAP 데이터 생성 (Plot 3, 4용)
export const generateUMAPData = () => {
  const cellTypes = ['Neuron', 'Cardiomyocyte', 'Hepatocyte', 'Alveolar', 'Epithelial', 'Fibroblast', 'Endothelial', 'Myocyte'];
  const umapData = [];
  
  cellTypes.forEach((cellType, idx) => {
    const nCells = 80 + Math.floor(Math.random() * 120);
    for (let i = 0; i < nCells; i++) {
      umapData.push({
        UMAP1: (Math.random() - 0.5) * 12 + (idx - 3.5) * 2.5,
        UMAP2: (Math.random() - 0.5) * 12 + Math.sin(idx * 0.8) * 4,
        celltype: cellType,
        CST3: Math.random() * 5,
        NKG7: Math.random() * 3,
        PECAM1: Math.random() * 4,
        CD3D: Math.random() * 3.5,
        GAPDH: Math.random() * 6
      });
    }
  });
  
  return umapData;
};
