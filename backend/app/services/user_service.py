from uuid import UUID
import uuid
from datetime import datetime, timezone

from fastapi.exceptions import HTTPException

from app.schemas.user import SUserCreate, SUserRead, SUserUpdate, SUserLogin, SToken
from app.dependencies import UserRepo

from passlib.hash import argon2

from app.utils.logger import logger

class UserService:
    async def get_users(self, user_repo: UserRepo):
        users = await user_repo.get_all()
        
        if not users:
            logger.error("Users is not found!")
            raise HTTPException(status_code=404, detail="Users is not found!")

        return users
    
    async def create_user(self, data: SUserCreate, user_repo: UserRepo) -> SUserRead:
        if data.password != data.password_verify:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        hashed_password = argon2.hash(data.password)
        
        user_dict = data.model_dump(exclude={"password", "password_verify"})
        user_dict["password_hash"] = hashed_password
        
        created_user = await user_repo.create(user_dict)
        if not created_user:
            logger.error("Users is not created!")
            raise HTTPException(status_code=500, detail="Users is not created!")

        return SUserRead.model_validate(created_user)
    
    async def login_user(self, data: SUserLogin, user_repo: UserRepo):
        exists_user = await user_repo.get_by_username(data.username)
        if not exists_user:
            raise HTTPException(status_code=500, detail="User is not registered")
        
        if not exists_user.password_hash: # type: ignore
            raise HTTPException(status_code=400, detail="User account is broken")
        
        verified = argon2.verify(data.password, exists_user.password_hash)
        if not verified:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        update_data = SUserUpdate(
            last_login_at=datetime.now(timezone.utc)
        ).model_dump(exclude_unset=True)
        
        updated_user = await user_repo.update(exists_user, update_data)
        if not updated_user:
            raise HTTPException(status_code=500, detail="Error while updating user")
        
        return {"public_id": str(exists_user.public_id)}
    
    async def register_user(self, data: SUserCreate, user_repo: UserRepo) -> str:
        if data.password != data.password_verify:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        hashed_password = argon2.hash(data.password)
        
        user_dict = data.model_dump(exclude={"password", "password_verify"})
        user_dict["password_hash"] = hashed_password
        user_dict["last_login_at"] = datetime.now(timezone.utc)
        
        try:
            created_user = await user_repo.create(user_dict)
            if not created_user:
                logger.error("Users is not created!")
                raise HTTPException(status_code=500, detail="Users is not created!")
            
            return str(created_user.public_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    # async def get_stage(
    #     self, 
    #     customer_id: UUID, 
    #     customer_repo: CustomerRepo, 
    #     lead_repo: RawLeadRepo
    # ) -> LeadStageType:
    #     inst_customer = await customer_repo.get_by_uuid(customer_id)
    #     if not inst_customer:
    #         logger.error("get_stage: Customer is not found!")
    #         raise HTTPException(status_code=404, detail="Customer is not found!")
        
    #     inst_lead = await lead_repo.get_latest_by_customer_id(inst_customer.id) # type: ignore
    #     if not inst_lead:
    #         logger.error("get_stage: Lead is not found!")
    #         raise HTTPException(status_code=404, detail="Lead is not found!")
            
    #     return LeadStageType(inst_lead.stage)
    
    # async def complete_application(
    #     self, 
    #     customer_id: UUID,
    #     data: SApplicationNewLead, 
    #     customer_repo: CustomerRepo, 
    #     lead_repo: LeadRepo,
    #     lead_status_history_repo: LeadStatusHistoryRepo
    # ):
    #     inst_customer = await customer_repo.get_by_uuid(customer_id)
    #     if not inst_customer:
    #         logger.error("complete_application: Customer is not found!")
    #         raise HTTPException(status_code=404, detail="Customer is not found!")
        
    #     profile_json = SProfileJsonData(
    #         credit_amount=data.credit_amount,
    #         credit_type=data.credit_type,
    #         city_name=data.city_name,
    #         income=data.income
    #     )
        
    #     inst_lead = await lead_repo.get_latest_by_customer_id(inst_customer.id) # type: ignore
    #     if not inst_lead:
    #         logger.error("complete_application: Lead is not found!")
    #         raise HTTPException(status_code=404, detail="Lead is not found!")
        
    #     lead_data = SLeadUpdate(
    #         stage=LeadStageType.SELFIE_IN_PROGRESS,
    #         stage_changed_at=datetime.now(timezone.utc),
    #         profile_json=profile_json.model_dump()
    #     )
        
    #     updated_lead = await lead_repo.update(inst_lead, lead_data.model_dump(exclude_unset=True))
    #     if not updated_lead:
    #         logger.error("complete_application: Lead is not updated!")
    #         raise HTTPException(status_code=500, detail="Lead is not updated!")
        
    #     status_history_data = SLeadStatusItemCreate(
    #         lead_id=updated_lead.id, # type: ignore
    #         from_stage=LeadStageType.PROFILE_IN_PROGRESS,
    #         to_stage=LeadStageType.SELFIE_IN_PROGRESS,
    #         source=LeadSource.FRONTEND
    #     )
        
    #     item = await lead_status_history_repo.create(status_history_data.model_dump())
    #     if not item:
    #         logger.error("complete_application: Lead Status History Item is not created!")
            
    #     card_data = SCardDescription(
    #         lead_id=updated_lead.id, # type: ignore
    #         iin=updated_lead.iin, # type: ignore
    #         phone=updated_lead.phone, # type: ignore
    #         stage=updated_lead.stage, # type: ignore
    #         income=profile_json.income,
    #         city_name=profile_json.city_name,
    #         credit_type=profile_json.credit_type,
    #         credit_amount=profile_json.credit_amount,
    #         metadata_json=updated_lead.metadata_json, # type: ignore
    #         other=updated_lead.other # type: ignore
    #     )
        
    #     await TrelloMan.update_card(updated_lead.id, card_data) # type: ignore
