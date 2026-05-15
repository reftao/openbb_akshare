"""China macro router extension."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.example import APIEx, PythonEx
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="", description="China macro data.")


@router.command(
    model="ChinaDR007",
    examples=[
        APIEx(parameters={"provider": "akshare"}),
        PythonEx(
            description="Get China DR007 Shibor data.",
            code=["result = obb.china_macro.dr007(provider='akshare')"],
        ),
    ],
)
async def dr007(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get China DR007 data."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="ChinaSocialFinancing",
    examples=[
        APIEx(parameters={"provider": "akshare"}),
        PythonEx(
            description="Get China social financing data.",
            code=["result = obb.china_macro.social_financing(provider='akshare')"],
        ),
    ],
)
async def social_financing(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get China social financing data."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="ChinaPMI",
    examples=[
        APIEx(parameters={"provider": "akshare"}),
        PythonEx(
            description="Get China PMI data.",
            code=["result = obb.china_macro.pmi(provider='akshare')"],
        ),
    ],
)
async def pmi(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get China PMI data."""
    return await OBBject.from_query(Query(**locals()))


@router.command(
    model="ChinaNorthboundFlow",
    examples=[
        APIEx(parameters={"provider": "akshare"}),
        PythonEx(
            description="Get China northbound flow data.",
            code=["result = obb.china_macro.northbound_flow(provider='akshare')"],
        ),
    ],
)
async def northbound_flow(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get China northbound flow data."""
    return await OBBject.from_query(Query(**locals()))
