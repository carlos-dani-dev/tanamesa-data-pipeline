from pydantic import BaseModel


class BeneficiariesSocioeconomicsStats(BaseModel):
    beneficiaries_on_vag: int
    beneficiaries_on_cadunico: int
    beneficiaries_on_cadunico_on_vag: int

class ConsistencyOfAccessRow(BaseModel):
    is_vag: bool
    freq_access: str
    total: int

class ConsistencyOfAccessResponse(BaseModel):
    consistency_of_access: list[ConsistencyOfAccessRow]

class ProgramDependencyRow(BaseModel):
    is_vag: bool
    is_dependent: bool
    total: int

class ProgramDependencyResponse(BaseModel):
    program_dependency: list[ProgramDependencyRow]

class ResidenceProgramServing(BaseModel):
    serving_status: str
    total: int

class EntireServedFamilyConfiguration(BaseModel):
    family_size: int
    total: int

class AssistedFamiliesResponse(BaseModel):
    residence_program_serving: list[ResidenceProgramServing]
    entire_served_family_configuration: list[EntireServedFamilyConfiguration]

class DifficultyOfAccessByRegion(BaseModel):
    region: str
    difficulty_type: str
    total: int

class LocalAccessResponse(BaseModel):
    difficulty_of_access_by_region: list[DifficultyOfAccessByRegion]

class BeneficiariesNotEatingStats(BaseModel):
    await_and_eat: int
    await_and_not_eat: int
    await_and_not_eat_on_vag: int