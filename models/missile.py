from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SCItemMissileParamsType, MissileInfo
from .base_model import HealthInfo, SHealthComponentParamsType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class Missile(MissileInfo):
    shop_info: list[ShopInfo]
    mass: float
    micro_scu: float
    size: int

    health_info: Optional[HealthInfo]

    class SpeedPhaseInfo(BaseModel):
        acceleration: float
        angular_acceleration: float
        angular_speed: float
        duration: float

    boost_phase: SpeedPhaseInfo
    intercept_phase: SpeedPhaseInfo
    terminal_phase: SpeedPhaseInfo
    lifetime: float


class MissileRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SCItemMissileParams: SCItemMissileParamsType
        SHealthComponentParams: Optional[SHealthComponentParamsType] = None
        SCItemPurchasableParams: Annotated[Optional[SCItemPurchasableParamsType], Field(alias="SCItemPurchasableParams")] = None

    Components: Components

    def to_missile(self) -> Missile:
        return Missile(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            size=self.Components.SAttachableComponentParams.AttachDef.Size,
            manufacturer=self.Components.SAttachableComponentParams.AttachDef.Manufacturer,
            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),

            shop_info=get_shop_info_by_ref(self.ref),
            mass=self.Components.SEntityPhysicsControllerParams.PhysType.Mass,
            micro_scu=self.Components.SAttachableComponentParams.AttachDef.inventoryOccupancyVolume.microSCU,
            health_info=HealthInfo.from_params(self.Components.SHealthComponentParams),
            damage=UniversalData.Damage(
                damage_biochemical=self.Components.SCItemMissileParams.explosionParams.damage.DamageBiochemical,
                damage_distortion=self.Components.SCItemMissileParams.explosionParams.damage.DamageDistortion,
                damage_energy=self.Components.SCItemMissileParams.explosionParams.damage.DamageEnergy,
                damage_physical=self.Components.SCItemMissileParams.explosionParams.damage.DamagePhysical,
                damage_thermal=self.Components.SCItemMissileParams.explosionParams.damage.DamageThermal,
                damage_stun=self.Components.SCItemMissileParams.explosionParams.damage.DamageStun,
            ),
            tracking_signal_type=self.Components.SCItemMissileParams.targetingParams.trackingSignalType,
            speed=self.Components.SCItemMissileParams.GCSParams.linearSpeed,
            arm_time=self.Components.SCItemMissileParams.armTime,
            lock_angle=self.Components.SCItemMissileParams.targetingParams.lockingAngle,
            lock_time=self.Components.SCItemMissileParams.targetingParams.lockTime,
            lock_range_min=self.Components.SCItemMissileParams.targetingParams.lockRangeMin,
            lock_range_max=self.Components.SCItemMissileParams.targetingParams.lockRangeMax,
            ignite_time=self.Components.SCItemMissileParams.igniteTime,
            lifetime=self.Components.SCItemMissileParams.maxLifetime,
            boost_phase=Missile.SpeedPhaseInfo(
                angular_speed=self.Components.SCItemMissileParams.GCSParams.boostPhase.angularSpeed,
                acceleration=self.Components.SCItemMissileParams.GCSParams.boostPhase.maxLinearAccelerationPositive.x,
                angular_acceleration=self.Components.SCItemMissileParams.GCSParams.boostPhase.maxRotationAccel,
                duration=self.Components.SCItemMissileParams.GCSParams.boostPhaseDuration,
            ),
            intercept_phase=Missile.SpeedPhaseInfo(
                angular_speed=self.Components.SCItemMissileParams.GCSParams.interceptPhase.angularSpeed,
                acceleration=self.Components.SCItemMissileParams.GCSParams.interceptPhase.maxLinearAccelerationPositive.x,
                angular_acceleration=self.Components.SCItemMissileParams.GCSParams.interceptPhase.maxRotationAccel,
                duration=0,
            ),
            terminal_phase=Missile.SpeedPhaseInfo(
                angular_speed=self.Components.SCItemMissileParams.GCSParams.terminalPhase.angularSpeed,
                acceleration=self.Components.SCItemMissileParams.GCSParams.terminalPhase.maxLinearAccelerationPositive.x,
                angular_acceleration=self.Components.SCItemMissileParams.GCSParams.terminalPhase.maxRotationAccel,
                duration=0,
            ),
            explosion_radius_min=self.Components.SCItemMissileParams.explosionParams.minRadius,
            explosion_radius_max=self.Components.SCItemMissileParams.explosionParams.maxRadius,
        )