from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, Extra


class Engine(Enum):
    SciML = "SciML"
    CIEMSS = "CIEMSS"


class Timespan(BaseModel):
    start: int = Field(..., example=1672531200)
    end: int = Field(..., example=1703980800)


class Status(Enum):
    queued = "queued"
    running = "started"
    complete = "finished"
    error = "error"


class Extra(BaseModel):
    class Config:
        extra = Extra.allow

    num_samples: Optional[int] = Field(
        None, description="number of samples for a CIEMSS simulation", example=100
    )


class Dataset(BaseModel):
    id: str = Field(None, example="cd339570-047d-11ee-be55")
    filename: str = Field(None, example="dataset.csv")


class SimulatePostRequest(BaseModel):
    engine: Engine = Field(..., example="CIEMSS")
    model_config_id: str = Field(..., example="ba8da8d4-047d-11ee-be56")
    timespan: Timespan
    extra: Extra = Field(
        None,
        description="optional extra system specific arguments for advanced use cases",
    )


class SimulatePostResponse(BaseModel):
    simulation_id: Optional[str] = Field(
        None,
        description="Simulation created successfully",
        example="fc5d80e4-0483-11ee-be56",
    )


class CalibratePostRequest(BaseModel):
    engine: Engine = Field(..., example="CIEMSS")
    model_config_id: str = Field(..., example="c1cd941a-047d-11ee-be56")
    dataset: Dataset = None
    timespan: Optional[Timespan] = None
    extra: Extra = Field(
        None,
        description="optional extra system specific arguments for advanced use cases",
    )


class CalibratePostResponse(BaseModel):
    simulation_id: Optional[str] = Field(
        None,
        description="Simulation created successfully",
        example="fc5d80e4-0483-11ee-be56",
    )


class EnsemblePostRequest(BaseModel):
    engine: Engine = Field(..., example="CIEMSS")
    model_configuration_ids: Optional[List[str]] = Field(
        None,
        example=[
            "ba8da8d4-047d-11ee-be56",
            "c1cd941a-047d-11ee-be56",
            "c4b9f88a-047d-11ee-be56",
        ],
    )
    timespan: Timespan
    num_samples: Optional[int] = Field(
        None, description="number of samples for a CIEMSS simulation", example=100
    )
    extra: Optional[Dict[str, Any]] = Field(
        None,
        description="optional extra system specific arguments for advanced use cases",
    )


class EnsemblePostResponse(BaseModel):
    simulation_id: Optional[str] = Field(
        None,
        description="Simulation created successfully",
        example="fc5d80e4-0483-11ee-be56",
    )


class StatusSimulationIdGetResponse(BaseModel):
    status: Optional[Status] = None
