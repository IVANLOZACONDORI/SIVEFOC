from pydantic import BaseModel, EmailStr, Field

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class InstitutionInput(BaseModel):
    code: str = Field(min_length=2,max_length=40,pattern=r'^[A-Za-z0-9_-]+$')
    name: str = Field(min_length=3,max_length=180)

class ProgramInput(BaseModel):
    code: str = Field(min_length=2,max_length=40)
    title: str = Field(min_length=3,max_length=200)

class CompetencyInput(BaseModel):
    code: str = Field(min_length=2,max_length=40)
    title: str = Field(min_length=3,max_length=200)
    description: str = Field(default='', max_length=2000)
    level: str = Field(default='general', max_length=40)
    program_id: str | None = None
