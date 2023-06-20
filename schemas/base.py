import enum
from typing import Annotated
from pydantic import AliasChoices, BaseModel, Field

from schemas.fields import PostCodeAnnotation


class ApReason(enum.Enum):
    ASP = "ASP"
    EHC = "EHC"
    MHN = "MHN"
    NEW = "NEW"
    OTH = "OTH"
    PEX = "PEX"
    PHN = "PHN"
    RHE = "RHE"


class SenReason(enum.Enum):
    N = "N"
    E = "E"
    K = "K"
    S = "S"
    A = "A"
    P = "P"


class BaseSchoolCensus(BaseModel):
    native_id: str = Field(alias="NativeId")
    source_id: str = Field(alias="sourceid")


class Address(BaseSchoolCensus):
    """
    Some detailed description of this model can be here
    """

    table_id: str = Field(
        validation_alias=AliasChoices("addressestableid", "someothername", "table_id")
    )
    addresses_order_seq_column: str = Field(alias="addressesorderseqcolumn")
    pupil_on_roll_table_id: str = Field(alias="pupilonrolltableid")
    uniquepropertyreferencenumber: int | None = Field(gt=10, lt=1000)
    postcode: Annotated[str, PostCodeAnnotation] | None
    saon: str | None = Field(min_length=3, max_length=10, pattern=r"^\d*$")
    paon: str | None
    street: str | None
    locality: str | None
    town: str | None
    administrativearea: str | None
    posttown: str | None
    addressline1: str | None
    addressline2: str | None
    addressline3: str | None
    addressline4: str | None
    addressline5: str | None

    class Config:
        arbitrary_types_allowed = True
        title = "address"


class ApprovisionDetail(BaseSchoolCensus):
    """
    Some detailed description of this model can be here
    """

    prevurn: str | None
    apreason: ApReason | None
    senprovisionentry: SenReason | None


class ApprovisionDetailOffRoll(ApprovisionDetail):
    """
    Some detailed description of this model can be here
    """

    table_id: str = Field(alias="approvisiondetailoffrolltableid")
    approvisiondetailoffrollorderseqcolumn: str
    pupilnolongeronrolltableid: str

    class Config:
        title = "approvisiondetailoffrole"


class ApprovisionDetailOnRoll(ApprovisionDetail):
    """
    Some detailed description of this model can be here
    """

    table_id: str = Field(alias="approvisiondetailonrolltableid")
    approvisiondetailonrollorderseqcolumn: str
    pupilonrolltableid: str

    class Config:
        title = "approvisiondetailonrole"


class SpringSchoolCensusDataset(BaseModel):
    """
    Some detailed description of this dataset can be here
    """

    address: Address = Field(alias="addresses.csv")
    approvisiondetailoffroll: ApprovisionDetailOffRoll = Field(
        alias="approvisiondetailoffroll.csv"
    )
    approvisiondetailonroll: ApprovisionDetailOnRoll = Field(
        alias="approvisiondetailonroll.csv"
    )

    class Config:
        title = "springschoolcensus"
