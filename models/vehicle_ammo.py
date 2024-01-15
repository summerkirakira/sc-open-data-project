from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .fps_ammo import FPSAmmo


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
    __polymorphicType: str
    __type: str
    accThrust: float
    aiNavigationType: str
    airResistance: float
    constantOrientation: bool
    decoupleHeading: bool
    disableGravity: bool
    noImpulse: bool
    noPathAlignment: bool
    noRoll: bool
    noSelfCollision: bool
    noSpin: bool
    pierceability: int
    radius: float
    rayCollision: bool
    singleContact: bool
    surfaceIdName: str
    thickness: float
    traceable: bool


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
    damage: Damage
    hitBehaviors: List
    hitType: str
    ignitionChanceOverride: float
    impactRadius: float
    keepAliveOnZeroDamage: bool
    minImpactRadius: float
    pierceabilityParams: PierceabilityParams
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


class VehicleAmmo(FPSAmmo):
    pass


class VehicleAmmoRaw(BaseModel):
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

    def to_vehicle_ammo(self) -> VehicleAmmo:
        return VehicleAmmo(
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
                damage_biochemical=0,
                damage_distortion=0,
                damage_energy=0,
                damage_physical=0,
                damage_stun=0,
                damage_thermal=0
            ),
            damage_drop_min_distance=FPSAmmo.DamageDropMinDistance(
                damage_biochemical=0,
                damage_distortion=0,
                damage_energy=0,
                damage_physical=0,
                damage_stun=0,
                damage_thermal=0
            ),
            damage_drop_per_meter=FPSAmmo.DamageDropPerMeter(
                damage_biochemical=0,
                damage_distortion=0,
                damage_energy=0,
                damage_physical=0,
                damage_stun=0,
                damage_thermal=0),
            ref=self.ref,
            path=self.path,
            type=self.type,
            chinese_name=self.path.split('/')[-1].split('.')[0],
            name=self.path.split('/')[-1].split('.')[0]
        )