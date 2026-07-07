from sqlalchemy import JSON, Column, Integer,Float, String, Boolean, DateTime, BigInteger
from .connection import Base
from datetime import datetime, UTC


class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)

    dur = Column(Float)
    proto = Column(String)
    service = Column(String)
    state = Column(String)

    spkts = Column(Integer)
    dpkts = Column(Integer)
    sbytes = Column(Integer)
    dbytes = Column(Integer)

    rate = Column(Float)

    sttl = Column(Integer)
    dttl = Column(Integer)

    sload = Column(Float)
    dload = Column(Float)

    sloss = Column(Integer)
    dloss = Column(Integer)

    sinpkt = Column(Float)
    dinpkt = Column(Float)

    sjit = Column(Float)
    djit = Column(Float)

    swin = Column(Integer)
    stcpb = Column(BigInteger)
    dtcpb = Column(BigInteger)
    dwin = Column(Integer)

    tcprtt = Column(Float)
    synack = Column(Float)
    ackdat = Column(Float)

    smean = Column(Integer)
    dmean = Column(Integer)

    trans_depth = Column(Integer)
    response_body_len = Column(Integer)

    ct_srv_src = Column(Integer)
    ct_state_ttl = Column(Integer)
    ct_dst_ltm = Column(Integer)
    ct_src_dport_ltm = Column(Integer)
    ct_dst_sport_ltm = Column(Integer)
    ct_dst_src_ltm = Column(Integer)

    is_ftp_login = Column(Integer)
    ct_ftp_cmd = Column(Integer)
    ct_flw_http_mthd = Column(Integer)

    ct_src_ltm = Column(Integer)
    ct_srv_dst = Column(Integer)

    is_sm_ips_ports = Column(Integer)

    attack_cat = Column(String)
    label = Column(Integer)


class PredictionResults(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
    DateTime(timezone=True),
    default=lambda: datetime.now(UTC),
    nullable=False)
    status = Column(
        String,
        default="pending",
        nullable=False
    )
    input_data = Column(JSON)
    predicted_label = Column(Boolean)
    confidence = Column(Float)