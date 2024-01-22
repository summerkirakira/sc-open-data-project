from __future__ import annotations

from typing import List, Optional

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


class FlareAmmo(UniversalData):
    mass: float
    lifetime: float


class FlareRaw(BaseModel):
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

    def to_vehicle_ammo(self) -> FlareAmmo:
        return FlareAmmo(
            mass=self.physicsControllerParams.PhysType.Mass,
            lifetime=self.lifetime,
            ref=self.ref,
            path=self.path,
            type=self.type,
            chinese_name=self.path.split('/')[-1].split('.')[0],
            name=self.path.split('/')[-1].split('.')[0]
        )