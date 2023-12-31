# View for the ecgs controller

from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session

from model.schemas import ECGModel, ECGZeroCrossingsModel, LeadModel
from model.models import ECGDBModel, LeadDBModel, UserDBModel

from controller.users import user_service
from controller.ecgs import egs_service
from controller.db import db_service


app = FastAPI()
router = APIRouter()


@router.post("/post-ecg")
async def post_ecg(
    ecg: ECGModel,
    db: Session = Depends(db_service.get_db),
    current_user: UserDBModel = Depends(user_service.get_current_user),
):
    """
    Writes an electrocardiogram into the database.

    Args:
        ecg (ECGModel): Electrocardiogram data.
        db (Session): Database session.
        current_user (UserDBModel): Current user.

    Returns:
        dict: Success message.
    """
    if current_user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    if ecg.id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manually passing 'id' for ECG is forbidden. ")

    leads = []
    for lead_data in ecg.leads:
        if lead_data.id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manually passing 'id' for Lead is forbidden. ")
        leads.append(LeadDBModel(**lead_data.dict()))

    db_ecg = ECGDBModel(
        date=ecg.date, user_id=current_user.username, leads=leads)

    try:
        db.add(db_ecg)
        db.commit()
        db.refresh(db_ecg)  # Refresh to get the updated 'db_ecg.id'
        return {"message": "ECG received successfully", "ecg_id": db_ecg.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()


@router.get("/get-ecg/{ecg_id}", response_model=ECGZeroCrossingsModel)
async def get_ecg(
    ecg_id: str,
    db: Session = Depends(db_service.get_db),
    current_user: UserDBModel = Depends(user_service.get_current_user),
    ecg_service=egs_service
):
    """
    Reads an electrocardiogram from the database.

    Args:
        ecg_id (str): Id of the electrocardiogram.
        db (Session): Database session.
        current_user (UserDBModel): Current user.
        ecg_service (EcgService): The ECG service.

    Returns:
        ECGZeroCrossingsModel: An electrocardiogram model object.
    """
    db_ecg = db.query(ECGDBModel).filter(ECGDBModel.id == ecg_id).first()

    # Check if the ECG exists
    if db_ecg is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ECG not found"
        )

    # Check if the current user has permission to access the ECG
    if current_user.username != db_ecg.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )

    # Use the ecg_service to calculate zero crossings on the fly
    zero_crossings = ecg_service.calculate_zero_crossings(db_ecg.leads)

    # Convert LeadDBModel instances to LeadModel instances
    leads = [
        LeadModel(
            id=lead.id,
            name=lead.name,
            samples=lead.samples,
            signal=lead.signal,
        )
        for lead in db_ecg.leads
    ]

    # Return the response with calculated zero crossings
    response_model = ECGZeroCrossingsModel(
        id=db_ecg.id,
        date=db_ecg.date,
        leads=leads,
        zerocrossings=zero_crossings,
    )

    return response_model
