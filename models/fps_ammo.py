from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field
from .base_model import UniversalData


class DiffuseColor(BaseModel):
    __type: str
    b: float
    g: float
    r: float


class LightPoolParams(BaseModel):
    __type: str
    animPhase: int
    animSpeed: float
    attenuationBulbSize: float
    autoClip: bool
    diffuseColor: DiffuseColor
    diffuseMultiplier: float
    fake: bool
    flareLensOpticsFrustumAngle: int
    flareName: str
    flareScale: float
    radius: float
    rampTime: float
    specularMultiplier: float
    style: int


class PhysType(BaseModel):
    Mass: float
    # __polymorphicType: str
    # __type: str
    # accThrust: float
    # aiNavigationType: str
    # airResistance: float
    # breakableParams: Any
    # constantOrientation: bool
    # decoupleHeading: bool
    # disableGravity: bool
    # gameCollisionClass: Any
    # noImpulse: bool
    # noPathAlignment: bool
    # noRoll: bool
    # noSelfCollision: bool
    # noSpin: bool
    # pierceability: int
    # radius: float
    # rayCollision: bool
    # singleContact: bool
    # surfaceIdName: str
    # thickness: float
    # traceable: bool


class PhysicsControllerParams(BaseModel):
    PhysType: PhysType
    __polymorphicType: str
    __type: str


class ProjectileLoopStart(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class ProjectileLoopStop(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class Damage(BaseModel):
    DamageBiochemical: float
    DamageDistortion: float
    DamageEnergy: float
    DamagePhysical: float
    DamageStun: float
    DamageThermal: float
    __polymorphicType: str
    __type: str


class DamageDropMinDamage(BaseModel):
    DamageBiochemical: float
    DamageDistortion: float
    DamageEnergy: float
    DamagePhysical: float
    DamageStun: float
    DamageThermal: float
    __polymorphicType: str
    __type: str


class DamageDropMinDistance(BaseModel):
    DamageBiochemical: float
    DamageDistortion: float
    DamageEnergy: float
    DamagePhysical: float
    DamageStun: float
    DamageThermal: float
    __polymorphicType: str
    __type: str


class DamageDropPerMeter(BaseModel):
    DamageBiochemical: float
    DamageDistortion: float
    DamageEnergy: float
    DamagePhysical: float
    DamageStun: float
    DamageThermal: float
    __polymorphicType: str
    __type: str


class DamageDropParams(BaseModel):
    __type: str
    damageDropMinDamage: DamageDropMinDamage
    damageDropMinDistance: DamageDropMinDistance
    damageDropPerMeter: DamageDropPerMeter


class ImpulseFalloffParams(BaseModel):
    __type: str
    dropFalloff: float
    maxFalloff: float
    minDistance: float


class PierceabilityParams(BaseModel):
    __type: str
    damageFalloffLevel1: float
    damageFalloffLevel2: float
    damageFalloffLevel3: float
    maxPenetrationThickness: float


class Material(BaseModel):
    __polymorphicType: str
    __type: str
    path: str


class VisualParams(BaseModel):
    Material: Material
    __type: str
    geometryRadius: float
    hitEffect: str
    maxLength: float
    meshOffset: float
    renderFrequency: int
    renderProbability: float


class ProjectileParams(BaseModel):
    __polymorphicType: str
    __type: str
    additionalProjectilesParams: Any
    alternateVisualParams: Any
    damage: Damage
    damageDropParams: DamageDropParams
    detonationParams: Any
    electronParams: Any
    hitBehaviors: List
    hitType: str
    ignitionChanceOverride: float
    impactRadius: float
    impulseFalloffParams: Optional[ImpulseFalloffParams] = None
    keepAliveOnZeroDamage: bool
    minImpactRadius: float
    pierceabilityParams: PierceabilityParams
    proximityTriggerParams: Any
    visualParams: VisualParams


class RicochetSound(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class TrailParticles(BaseModel):
    __polymorphicType: str
    __type: str
    path: str


class WhizSound(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class FPSAmmo(UniversalData):
    mass: float
    lifetime: float

    class Damage(BaseModel):
        damage_biochemical: float
        damage_distortion: float
        damage_energy: float
        damage_physical: float
        damage_stun: float
        damage_thermal: float

    class DamageDropMinDamage(BaseModel):
        damage_biochemical: float
        damage_distortion: float
        damage_energy: float
        damage_physical: float
        damage_stun: float
        damage_thermal: float

    class DamageDropMinDistance(BaseModel):
        damage_biochemical: float
        damage_distortion: float
        damage_energy: float
        damage_physical: float
        damage_stun: float
        damage_thermal: float

    class DamageDropPerMeter(BaseModel):
        damage_biochemical: float
        damage_distortion: float
        damage_energy: float
        damage_physical: float
        damage_stun: float
        damage_thermal: float

    damage: Damage
    damage_drop_min_damage: DamageDropMinDamage
    damage_drop_min_distance: DamageDropMinDistance
    damage_drop_per_meter: DamageDropPerMeter


class FPSAmmoRaw(BaseModel):
    UIIconType: str
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')
    ammoCategory: str
    bulletType: int
    displayName: str
    hitPoints: float
    impulseScale: float
    inheritVelocity: float
    lifetime: float
    lightPoolParams: LightPoolParams
    noBulletHits: bool
    physicsControllerParams: PhysicsControllerParams
    projectileLoopStart: ProjectileLoopStart
    projectileLoopStop: ProjectileLoopStop
    projectileParams: ProjectileParams
    quietRemoval: bool
    ricochetSound: RicochetSound
    shotsPerAudioLoop: int
    showtime: float
    size: int
    spawnType: str
    speed: float
    trailParticles: TrailParticles
    useInConvergence: bool
    whizSound: WhizSound
    whizSoundDistance: float

    def to_fps_ammo(self) -> FPSAmmo:
        return FPSAmmo(
            mass=self.physicsControllerParams.PhysType.Mass,
            lifetime=self.lifetime,
            damage=FPSAmmo.Damage(
                damage_biochemical=self.projectileParams.damage.DamageBiochemical,
                damage_distortion=self.projectileParams.damage.DamageDistortion,
                damage_energy=self.projectileParams.damage.DamageEnergy,
                damage_physical=self.projectileParams.damage.DamagePhysical,
                damage_stun=self.projectileParams.damage.DamageStun,
                damage_thermal=self.projectileParams.damage.DamageThermal
            ),
            damage_drop_min_damage=FPSAmmo.DamageDropMinDamage(
                damage_biochemical=self.projectileParams.damageDropParams.damageDropMinDamage.DamageBiochemical,
                damage_distortion=self.projectileParams.damageDropParams.damageDropMinDamage.DamageDistortion,
                damage_energy=self.projectileParams.damageDropParams.damageDropMinDamage.DamageEnergy,
                damage_physical=self.projectileParams.damageDropParams.damageDropMinDamage.DamagePhysical,
                damage_stun=self.projectileParams.damageDropParams.damageDropMinDamage.DamageStun,
                damage_thermal=self.projectileParams.damageDropParams.damageDropMinDamage.DamageThermal
            ),
            damage_drop_min_distance=FPSAmmo.DamageDropMinDistance(
                damage_biochemical=self.projectileParams.damageDropParams.damageDropMinDistance.DamageBiochemical,
                damage_distortion=self.projectileParams.damageDropParams.damageDropMinDistance.DamageDistortion,
                damage_energy=self.projectileParams.damageDropParams.damageDropMinDistance.DamageEnergy,
                damage_physical=self.projectileParams.damageDropParams.damageDropMinDistance.DamagePhysical,
                damage_stun=self.projectileParams.damageDropParams.damageDropMinDistance.DamageStun,
                damage_thermal=self.projectileParams.damageDropParams.damageDropMinDistance.DamageThermal
            ),
            damage_drop_per_meter=FPSAmmo.DamageDropPerMeter(
                damage_biochemical=self.projectileParams.damageDropParams.damageDropPerMeter.DamageBiochemical,
                damage_distortion=self.projectileParams.damageDropParams.damageDropPerMeter.DamageDistortion,
                damage_energy=self.projectileParams.damageDropParams.damageDropPerMeter.DamageEnergy,
                damage_physical=self.projectileParams.damageDropParams.damageDropPerMeter.DamagePhysical,
                damage_stun=self.projectileParams.damageDropParams.damageDropPerMeter.DamageStun,
                damage_thermal=self.projectileParams.damageDropParams.damageDropPerMeter.DamageThermal),
            ref=self.ref,
            path=self.path,
            type=self.type,
            chinese_name=self.path.split('/')[-1].split('.')[0],
            name=self.path.split('/')[-1].split('.')[0]
        )
