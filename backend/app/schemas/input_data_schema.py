from pydantic import BaseModel, Field
from typing import Optional



class InputDataSchema(BaseModel):
    """
      A pydantic model for representing input data for prediction. 
    """
    # REQUIRED FEATURES
    proto: str
    service: str
    state: str

    dur: float = Field(ge=0)

    spkts: int = Field(ge=0)
    dpkts: int = Field(ge=0)

    sbytes: int = Field(ge=0)
    dbytes: int = Field(ge=0)

    rate: float = Field(ge=0)

    sttl: int = Field(ge=0)
    dttl: int = Field(ge=0)

    sload: float = Field(ge=0)
    dload: float = Field(ge=0)

    sloss: int = Field(ge=0)
    dloss: int = Field(ge=0)

    sinpkt: float = Field(ge=0)
    dinpkt: float = Field(ge=0)

    sjit: float = Field(ge=0)
    djit: float = Field(ge=0)

    swin: int = Field(ge=0)

    tcprtt: float = Field(ge=0)
    synack: float = Field(ge=0)
    ackdat: float = Field(ge=0)

    smean: int = Field(ge=0)
    dmean: int = Field(ge=0)

    ct_srv_src: int = Field(ge=0)
    ct_state_ttl: int = Field(ge=0)
    ct_dst_ltm: int = Field(ge=0)
    ct_src_dport_ltm: int = Field(ge=0)
    ct_dst_sport_ltm: int = Field(ge=0)
    ct_dst_src_ltm: int = Field(ge=0)
    ct_srv_dst: int = Field(ge=0)

    # OPTIONAL FEATURES

    stcpb: Optional[int] = None
    dtcpb: Optional[int] = None
    dwin: Optional[int] = None

    trans_depth: Optional[int] = None
    response_body_len: Optional[int] = None

    is_ftp_login: Optional[int] = None
    ct_ftp_cmd: Optional[int] = None
    ct_flw_http_mthd: Optional[int] = None

    ct_src_ltm: Optional[int] = None
    is_sm_ips_ports: Optional[int] = None
