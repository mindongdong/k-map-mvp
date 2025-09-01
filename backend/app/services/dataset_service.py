"""
Dataset service layer
Business logic for dataset CRUD operations
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetUpdate


class DatasetService:
    """Service class for dataset operations"""
    
    @staticmethod
    def get_dataset_by_id(db: Session, dataset_id: int) -> Optional[Dataset]:
        """Get dataset by internal ID"""
        return db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
    
    @staticmethod
    def get_dataset_by_public_id(db: Session, public_dataset_id: str) -> Optional[Dataset]:
        """Get dataset by public ID (HBM123.ABCD.456)"""
        return db.query(Dataset).filter(Dataset.public_dataset_id == public_dataset_id).first()
    
    @staticmethod
    def get_datasets(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        group_name: Optional[str] = None,
        data_type: Optional[str] = None,
        organ: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "publication_date",
        sort_order: str = "desc"
    ) -> List[Dataset]:
        """
        Get datasets with filtering, searching, and sorting
        
        Args:
            db: Database session
            skip: Offset for pagination
            limit: Maximum number of results
            group_name: Filter by research group
            data_type: Filter by data type
            organ: Filter by organ
            status: Filter by status
            search: Search in description, citation, and group_name
            sort_by: Field to sort by
            sort_order: 'asc' or 'desc'
        """
        query = db.query(Dataset)
        
        # Apply filters
        filters = []
        if group_name:
            filters.append(Dataset.group_name.ilike(f"%{group_name}%"))
        if data_type:
            filters.append(Dataset.data_type.ilike(f"%{data_type}%"))
        if organ:
            filters.append(Dataset.organ.ilike(f"%{organ}%"))
        if status:
            filters.append(Dataset.status == status)
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Apply search
        if search:
            search_filter = or_(
                Dataset.description.ilike(f"%{search}%"),
                Dataset.citation.ilike(f"%{search}%"),
                Dataset.group_name.ilike(f"%{search}%"),
                Dataset.public_dataset_id.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Apply sorting
        sort_column = getattr(Dataset, sort_by, Dataset.publication_date)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_datasets_count(
        db: Session,
        group_name: Optional[str] = None,
        data_type: Optional[str] = None,
        organ: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> int:
        """Get total count of datasets with same filters as get_datasets"""
        query = db.query(Dataset)
        
        # Apply same filters as get_datasets
        filters = []
        if group_name:
            filters.append(Dataset.group_name.ilike(f"%{group_name}%"))
        if data_type:
            filters.append(Dataset.data_type.ilike(f"%{data_type}%"))
        if organ:
            filters.append(Dataset.organ.ilike(f"%{organ}%"))
        if status:
            filters.append(Dataset.status == status)
        
        if filters:
            query = query.filter(and_(*filters))
        
        if search:
            search_filter = or_(
                Dataset.description.ilike(f"%{search}%"),
                Dataset.citation.ilike(f"%{search}%"),
                Dataset.group_name.ilike(f"%{search}%"),
                Dataset.public_dataset_id.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.count()
    
    @staticmethod
    def create_dataset(db: Session, dataset: DatasetCreate, uploader_id: int) -> Dataset:
        """Create new dataset"""
        # Generate unique public dataset ID if not provided
        if not hasattr(dataset, 'public_dataset_id') or not dataset.public_dataset_id:
            # Simple ID generation - in production, use more sophisticated method
            count = db.query(Dataset).count()
            public_id = f"HBM{count + 1:03d}.AUTO.{datetime.now().strftime('%m%d')}"
        else:
            public_id = dataset.public_dataset_id
        
        db_dataset = Dataset(
            public_dataset_id=public_id,
            uploader_id=uploader_id,
            group_name=dataset.group_name,
            data_type=dataset.data_type,
            organ=dataset.organ,
            status=dataset.status or "Draft",
            publication_date=dataset.publication_date,
            description=dataset.description,
            citation=dataset.citation,
            file_storage_path=dataset.file_storage_path
        )
        
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        return db_dataset
    
    @staticmethod
    def update_dataset(
        db: Session, 
        public_dataset_id: str, 
        dataset_update: DatasetUpdate
    ) -> Optional[Dataset]:
        """Update existing dataset"""
        db_dataset = DatasetService.get_dataset_by_public_id(db, public_dataset_id)
        if not db_dataset:
            return None
        
        # Update fields
        update_data = dataset_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_dataset, field, value)
        
        db_dataset.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_dataset)
        return db_dataset
    
    @staticmethod
    def delete_dataset(db: Session, public_dataset_id: str) -> bool:
        """Delete dataset by public ID"""
        db_dataset = DatasetService.get_dataset_by_public_id(db, public_dataset_id)
        if not db_dataset:
            return False
        
        db.delete(db_dataset)
        db.commit()
        return True
    
    @staticmethod
    def get_dataset_statistics(db: Session) -> dict:
        """Get dataset statistics"""
        total_datasets = db.query(Dataset).count()
        
        # Group by data type
        data_types = db.query(Dataset.data_type).distinct().all()
        data_type_counts = {}
        for (data_type,) in data_types:
            count = db.query(Dataset).filter(Dataset.data_type == data_type).count()
            data_type_counts[data_type] = count
        
        # Group by organ
        organs = db.query(Dataset.organ).distinct().all()
        organ_counts = {}
        for (organ,) in organs:
            count = db.query(Dataset).filter(Dataset.organ == organ).count()
            organ_counts[organ] = count
        
        # Group by status
        statuses = db.query(Dataset.status).distinct().all()
        status_counts = {}
        for (status,) in statuses:
            count = db.query(Dataset).filter(Dataset.status == status).count()
            status_counts[status] = count
        
        # Group by research group
        groups = db.query(Dataset.group_name).distinct().all()
        group_counts = {}
        for (group_name,) in groups:
            count = db.query(Dataset).filter(Dataset.group_name == group_name).count()
            group_counts[group_name] = count
        
        return {
            "total_datasets": total_datasets,
            "by_data_type": data_type_counts,
            "by_organ": organ_counts,
            "by_status": status_counts,
            "by_research_group": group_counts
        }