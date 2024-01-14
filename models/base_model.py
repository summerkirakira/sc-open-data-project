from pydantic import BaseModel
from typing import List, Optional, Literal
from utils.localizer import localizer_cn, localizer_en
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class UniversalData(BaseModel):
    type: str
    name: str
    chinese_name: Optional[str]
    description: Optional[str] = None
    chinese_description: Optional[str] = None
    ref: str
    size: int = 0


    class Damage(BaseModel):
        damage_biochemical: float
        damage_distortion: float
        damage_energy: float
        damage_physical: float
        damage_stun: float
        damage_thermal: float


class SAttachableComponentParams(BaseModel):
    class AttachDef(BaseModel):

        class InventoryOccupancyVolume(BaseModel):
            __polymorphicType: str
            __type: str
            microSCU: int

        class MannequinTags(BaseModel):
            __type: str
            mannequinBaseTag: str
            mannequinClassTag: str
            mannequinTypeTag: str

        class Localization(BaseModel):
            class DisplayFeatures(BaseModel):
                Callout1: str
                Callout2: str
                Callout3: str
                FrontendBackground: str
                History: str
                LogoSimplifiedWhite: str
                UIPriority: int
                __type: str

            Description: str
            Name: str
            ShortName: str
            __type: str
            displayFeatures: DisplayFeatures


        DisplayType: str
        Grade: int
        Localization: Localization
        Manufacturer: str
        RequiredTags: str
        Size: int
        SubType: str
        Tags: str
        Type: str
        __type: str
        ignoredAttachAxis: str
        inheritParentManufacturer: bool
        inventoryOccupancyVolume: InventoryOccupancyVolume
        mannequinTags: MannequinTags

    AttachDef: AttachDef
    __polymorphicType: str
    __type: str
    attachToTileItemPort: str
    entityAttachParams: Optional[str] = None


class SEntityPhysicsControllerParams(BaseModel):
    class PhysType(BaseModel):
        class Temperature(BaseModel):
            class SignatureParams(BaseModel):
                __type: str
                enable: bool
                minimumTemperatureForIR: float
                temperatureToIR: float

            class MisfireTemperatureRange(BaseModel):
                __type: str
                maximum: float
                minimum: float

            class ItemResourceParams(BaseModel):
                __type: str
                enableOverheat: bool
                minCoolingTemperature: float
                minOperatingTemperature: float
                overheatRecoveryTemperature: float
                overheatTemperature: float
                overheatWarningTemperature: float

            __type: str
            enable: bool
            initialTemperature: float
            internalTemperatureGeneration: float
            itemResourceParams: ItemResourceParams
            misfireTemperatureRange: MisfireTemperatureRange
            signatureParams: SignatureParams

        Damping: float
        DampingFreefall: float
        EnableCrossGridChecks: bool
        Kinematic: bool
        Mass: float
        NeverAffectTriggers: bool
        PushableByPlayers: bool
        Resting: bool
        UseManualGridTransition: bool
        __polymorphicType: str
        __type: str
        aiNavigationType: str
        maxLoggedCollisions: int
        physicalizeAllSlots: bool
        temperature: Temperature

    PhysType: PhysType
    __polymorphicType: str
    __type: str


class SCItemPurchasableParamsType(BaseModel):

    __polymorphicType: str
    __type: str
    allowQuickBuy: bool
    allowTryOn: bool
    defaultAttachToPortName: str
    disabledLoadoutInteractions: List
    displayName: str
    displayThumbnail: str
    displayType: str
    interactionPointTemplate: str
    tryOnInteractionText: str





class StaticEntityClassData(BaseModel):
    class DefaultEntitlementEntityParams(BaseModel):
        __polymorphicType: str
        __type: str
        canEntitleThroughWebsite: bool
        entitlementPolicy: str

    class EntityUIDisplayParams(BaseModel):
        class TrackerProperties(BaseModel):
            __type: str

        __polymorphicType: str
        __type: str
        displayDescription: str
        displayIcon: str
        displayImage: str
        displayThumbnail: str
        sortString: str
        trackerProperties: TrackerProperties

    DefaultEntitlementEntityParams: Optional[DefaultEntitlementEntityParams] = None
    EntityUIDisplayParams: Optional[EntityUIDisplayParams] = None





class AimRTPC(BaseModel):
    __type: str
    rtpc: str


class AimStart(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class AimStop(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class DofSettings(BaseModel):
    __type: str
    blurAmount: float
    dofMinZ: float
    dofMinZScale: float
    fStop: float
    focusMax: float
    focusMin: float
    nearFocalDistance: float


class EntityTags(BaseModel):
    __type: str
    tags: List


class MannequinTag(BaseModel):
    __type: str
    tag: str


class SMannequinTagParams(BaseModel):
    __type: str
    tag: str


class MannequinTag1(BaseModel):
    SMannequinTagParams: SMannequinTagParams


class SwitchFireModeAudioTrigger(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class TimeSinceLastAimStartRtpc(BaseModel):
    __type: str
    rtpc: str


class TimeSinceLastAimStopRtpc(BaseModel):
    __type: str
    rtpc: str





class AimModifier(BaseModel):
    __type: str
    hideWeaponInADS: bool
    zoomScale: float
    zoomTimeScale: float


class SalvageModifier(BaseModel):
    __type: str
    extractionEfficiency: float
    radiusMultiplier: float
    salvageSpeedMultiplier: float


class HeatStats(BaseModel):
    __type: str
    aimModifier: AimModifier
    ammoCost: int
    ammoCostMultiplier: float
    burstShots: int
    chargeTimeMultiplier: float
    damageMultiplier: float
    damageOverTimeMultiplier: float
    fireRate: int
    fireRateMultiplier: float
    heatGenerationMultiplier: float
    pellets: int
    projectileSpeedMultiplier: float
    salvageModifier: SalvageModifier


class LaunchParams(BaseModel):
    class SpreadParams(BaseModel):
        __type: str
        attack: float
        decay: float
        firstAttack: float
        max: float
        min: float

    __polymorphicType: str
    __type: str
    ammoCost: int
    damageMultiplier: float
    fireHelper: str
    muzzleHelper: str
    pelletCount: int
    projectileType: str
    soundRadius: float
    spreadParams: SpreadParams

class SCItemWeaponComponentParams(BaseModel):
    class WeaponRegenConsumerParams(BaseModel):
        __type: str
        regenerationCooldown: float
        regenerationCostPerBullet: float
        requestedAmmoLoad: float
        requestedRegenPerSec: float

    class FireAction(BaseModel):
        class SWeaponActionFireSingleParamsType(BaseModel):
            fireRate: float
            heatPerShot: float
            aiShootingMode: str
            localisedName: str
            launchParams: LaunchParams

        class SWeaponActionFireRapidParamsType(BaseModel):
            fireRate: float
            heatPerShot: float
            aiShootingMode: str
            localisedName: str
            launchParams: LaunchParams

        class SWeaponActionFireBurstParamsType(BaseModel):
            fireRate: float
            heatPerShot: float
            aiShootingMode: str
            cooldownTime: float
            localisedName: str
            launchParams: LaunchParams

        class SWeaponActionFireChargedParamsType(BaseModel):

            chargeTime: float
            aiShootingMode: str
            localisedName: str

        SWeaponActionFireChargedParams: Optional[SWeaponActionFireChargedParamsType] = None
        SWeaponActionFireBurstParams: Optional[SWeaponActionFireBurstParamsType] = None
        SWeaponActionFireRapidParams: Optional[SWeaponActionFireRapidParamsType] = None
        SWeaponActionFireSingleParams: Optional[SWeaponActionFireSingleParamsType] = None

    class ConnectionParams(BaseModel):
        class SWeaponStats(BaseModel):
            class RecoilModifier(BaseModel):
                class CurveRecoil1(BaseModel):
                    class RotationModifiers(BaseModel):
                        class MaxLimitsModifier2(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class MinLimitsModifier2(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class NoiseModifier1(BaseModel):
                            __type: str
                            xNoiseModifier: float
                            yNoiseModifier: float
                            zNoiseModifier: float

                        __type: str
                        maxLimitsModifier: MaxLimitsModifier2
                        minLimitsModifier: MinLimitsModifier2
                        noiseModifier: NoiseModifier1
                        xMaxValueModifier: float
                        yMaxValueModifier: float
                        zMaxValueModifier: float

                    class RotationDecayModifiers(BaseModel):
                        class DecayMaxValueModifier1(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class DecayMinScalingFactorModifier1(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class DecayTimeMultiplierModifier1(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        __type: str
                        decayMaxValueModifier: DecayMaxValueModifier1
                        decayMinScalingFactorModifier: DecayMinScalingFactorModifier1
                        decayTimeMultiplierModifier: DecayTimeMultiplierModifier1

                    class PositionModifiers(BaseModel):
                        class MaxLimitsModifier1(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class MinLimitsModifier1(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class NoiseModifier(BaseModel):
                            __type: str
                            xNoiseModifier: float
                            yNoiseModifier: float
                            zNoiseModifier: float

                        __type: str
                        maxLimitsModifier: MaxLimitsModifier1
                        minLimitsModifier: MinLimitsModifier1
                        noiseModifier: NoiseModifier
                        xMaxValueModifier: float
                        yMaxValueModifier: float
                        zMaxValueModifier: float

                    class PositionDecayModifiers(BaseModel):
                        class DecayMaxValueModifier(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class DecayMinScalingFactorModifier(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class DecayTimeMultiplierModifier(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        __type: str
                        decayMaxValueModifier: DecayMaxValueModifier
                        decayMinScalingFactorModifier: DecayMinScalingFactorModifier
                        decayTimeMultiplierModifier: DecayTimeMultiplierModifier

                    __type: str
                    maxDecayTimeModifier: float
                    minDecayTimeModifier: float
                    positionDecayModifiers: PositionDecayModifiers
                    positionModifiers: PositionModifiers
                    recoilTimeModifier: float
                    rotationDecayModifiers: RotationDecayModifiers
                    rotationModifiers: RotationModifiers

                class CurveRecoilHead(BaseModel):
                    class RotationModifier(BaseModel):
                        class NoiseModifier3(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class OffsetModifier1(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        __type: str
                        noiseModifier: NoiseModifier3
                        offsetModifier: OffsetModifier1

                    class PositionModifier(BaseModel):
                        class OffsetModifier(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class NoiseModifier2(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        __type: str
                        noiseModifier: NoiseModifier2
                        offsetModifier: OffsetModifier

                    __type: str
                    frequencyModifier: float
                    headRecoilTimeModifier: float
                    positionModifier: PositionModifier
                    rotationModifier: RotationModifier
                    smoothingSpeedModifier: float

                class HeadRotationMultiplier(BaseModel):
                    __type: str
                    x: float
                    y: float
                    z: float

                class AimRecoilModifier(BaseModel):
                    class MaxMultiplier(BaseModel):
                        __type: str
                        x: float
                        y: float

                    class ShotKickFirstMultiplier(BaseModel):
                        __type: str
                        x: float
                        y: float

                    class ShotKickMultiplier(BaseModel):
                        __type: str
                        x: float
                        y: float

                    class CurveRecoil(BaseModel):
                        class AimModifier(BaseModel):
                            __type: str
                            hideWeaponInADS: bool
                            zoomScale: float
                            zoomTimeScale: float

                        class MaxLimitsModifier(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class MinLimitsModifier(BaseModel):
                            __type: str
                            x: float
                            y: float
                            z: float

                        class NoiseCurvesModifier(BaseModel):
                            __type: str
                            pitchNoiseMaxValueModifier: float
                            rollNoiseMaxValueModifier: float
                            yawNoiseMaxValueModifier: float

                        __type: str
                        decayStartTimeModifier: float
                        maxDecayTimeModifier: float
                        maxFireTimeModifier: float
                        maxLimitsModifier: MaxLimitsModifier
                        minDecayTimeModifier: float
                        minLimitsModifier: MinLimitsModifier
                        noiseCurvesModifier: NoiseCurvesModifier
                        pitchMaxDegreesModifier: float
                        recoilSmoothTimeModifier: float
                        rollMaxDegreesModifier: float
                        yawMaxDegreesModifier: float

                    __type: str
                    curveRecoil: CurveRecoil
                    decayMultiplier: float
                    endDecayMultiplier: float
                    maxMultiplier: MaxMultiplier
                    randomPitchMultiplier: float
                    randomYawMultiplier: float
                    shotKickFirstMultiplier: ShotKickFirstMultiplier
                    shotKickMultiplier: ShotKickMultiplier

                __type: str
                aimRecoilModifier: AimRecoilModifier
                angleRecoilStrengthMultiplier: float
                animatedRecoilMultiplier: float
                curveRecoil: CurveRecoil1
                curveRecoilHead: CurveRecoilHead
                decayMultiplier: float
                endDecayMultiplier: float
                fireRecoilStrengthFirstMultiplier: float
                fireRecoilStrengthMultiplier: float
                fireRecoilTimeMultiplier: float
                frontalOscillationDecayMultiplier: float
                frontalOscillationRandomnessMultiplier: float
                frontalOscillationRotationMultiplier: float
                frontalOscillationStrengthMultiplier: float
                headRotationMultiplier: HeadRotationMultiplier
                randomnessBackPushMultiplier: float
                randomnessMultiplier: float

            class SalvageModifier(BaseModel):
                __type: str
                extractionEfficiency: float
                radiusMultiplier: float
                salvageSpeedMultiplier: float

            class SpreadModifier(BaseModel):
                __type: str
                additiveModifier: float
                attackMultiplier: float
                decayMultiplier: float
                firstAttackMultiplier: float
                maxMultiplier: float
                minMultiplier: float

            __type: str
            aimModifier: AimModifier
            ammoCost: int
            ammoCostMultiplier: float
            burstShots: int
            chargeTimeMultiplier: float
            damageMultiplier: float
            damageOverTimeMultiplier: float
            fireRate: int
            fireRateMultiplier: float
            heatGenerationMultiplier: float
            pellets: int
            projectileSpeedMultiplier: float
            recoilModifier: RecoilModifier
            salvageModifier: SalvageModifier
            soundRadiusMultiplier: float
            spreadModifier: SpreadModifier
            useAlternateProjectileVisuals: bool
            useAugmentedRealityProjectiles: bool

        __type: str
        glowTag: str
        heatRateOnline: float
        heatReduceWhenOverheatIsFixed: float
        heatStats: HeatStats
        lockOnOnverheat: bool
        maxGlow: float
        overheatEffects: List
        powerActiveCooldown: float
        rangedHeatStats: List

        noPowerStats: SWeaponStats
        overclockStats: SWeaponStats
        overpowerStats: SWeaponStats
        underpowerStats: SWeaponStats


    class WeaponAIData(BaseModel):
        class AiFiringActionParam(BaseModel):
            class SWeaponAIChargedParams(BaseModel):
                class ChargeDurationInterval(BaseModel):
                    __type: str
                    maximum: float
                    minimum: float

                __polymorphicType: str
                __type: str
                aiShootingMode: str
                chargeDurationBeforeCoverAction: float
                chargeDurationInterval: ChargeDurationInterval
                name: str

            SWeaponAIChargedParams: SWeaponAIChargedParams

        class AccuracyRange(BaseModel):
            __type: str
            maximum: float
            minimum: float

        CombatRangeCategory: str
        __type: str
        accuracyRange: AccuracyRange
        aiFiringActionParams: List[AiFiringActionParam]
        baseAccuracy: float
        canShootWhenObstructed: bool
        idealCombatRange: float
        impactRadiusForFriendlyFire: float

    ShouldIgnorePrimaryAmmoContainer: bool
    actorProceduralRecoilConfig: str
    aimableAnglesRecord: str
    ammoContainerRecord: str
    autoAimMuzzleAngleOverwrite: float
    connectionParams: ConnectionParams
    gimbalModeModifierRecord: str
    isAllowedInGreenZones: bool
    secondaryAmmoContainers: List
    supplementaryFireTime: float
    turnedOnEffects: List
    uncollapseOnTurnedOn: bool
    useAdsHelper: bool
    weaponAIData: WeaponAIData
    weaponRegenConsumerParams: Optional[WeaponRegenConsumerParams] = None
    fireActions: List[FireAction]


class SCItemClothingParams(BaseModel):
    class OverlayTags(BaseModel):
        __type: str
        tags: List

    class RadiationResistance(BaseModel):
        MaximumRadiationCapacity: float
        RadiationDissipationRate: float
        __type: str

    class TemperatureResistance(BaseModel):
        MaxResistance: float
        MinResistance: float
        __type: str

    Chunks: List
    DressFragmentTags: str
    FoleyDef: str
    FootstepDef: str
    HiddenParts: List
    OverlayTags: OverlayTags
    RadiationResistance: RadiationResistance
    TemperatureResistance: TemperatureResistance


class SAmmoContainerComponentParamsType(BaseModel):
    class AmmoCountFragment(BaseModel):
        __type: str
        forceWeaponController: bool
        fragment: str

    allowAmmoRepool: bool
    ammoContainerType: str
    ammoCountAnimationBlendTime: float
    ammoCountFragment: AmmoCountFragment
    ammoParamsRecord: str
    attachableEntities: List
    despawnEmptyAmmoContainer: bool
    emptyGeometryTag: str
    hideAttachments: List
    initialAmmoCount: int
    maxAmmoCount: int
    maxRestockCount: int
    secondaryAmmoParamsRecord: str


class PurchaseInfo(BaseModel):
    name: str
    purchaseType: str
    shopInfo: None

    @classmethod
    def from_purchase_params(cls, purchase_params: Optional[SCItemPurchasableParamsType]) -> Optional['PurchaseInfo']:
        if purchase_params is None:
            return None
        return PurchaseInfo(
            name=localizer_cn.get(purchase_params.displayName),
            purchaseType=localizer_cn.get(purchase_params.displayType),
            shopInfo=None
        )


class MissileInfo(BaseModel):

    damage: UniversalData.Damage
    tracking_signal_type: Literal['CrossSection', 'Infrared', 'Electromagnetic']
    speed: float
    arm_time: float
    lock_angle: float
    lock_time: float
    lock_range_min: float
    lock_range_max: float
    ignite_time: float
    explosion_radius_min: float
    explosion_radius_max: float

    # shop_info: list[PurchaseInfo] = []


class SCItemMissileParamsType(BaseModel):
    class GCSParams(BaseModel):
        class BoostPhase(BaseModel):

            class MaxLinearAccelerationNegative(BaseModel):
                __type: str
                x: float
                y: float
                z: float

            class MaxLinearAccelerationPositive(BaseModel):
                __type: str
                x: float
                y: float
                z: float

            __type: str
            angularSpeed: float
            maxLinearAccelerationNegative: MaxLinearAccelerationNegative
            maxLinearAccelerationPositive: MaxLinearAccelerationPositive
            maxRotationAccel: float
            pidAggression: float

        class InterceptPhase(BaseModel):
            class MaxLinearAccelerationNegative1(BaseModel):
                __type: str
                x: float
                y: float
                z: float

            class MaxLinearAccelerationPositive1(BaseModel):
                __type: str
                x: float
                y: float
                z: float

            __type: str
            angularSpeed: float
            maxLinearAccelerationNegative: MaxLinearAccelerationNegative1
            maxLinearAccelerationPositive: MaxLinearAccelerationPositive1
            maxRotationAccel: float
            pidAggression: float

        class TerminalPhase(BaseModel):
            class MaxLinearAccelerationPositive2(BaseModel):
                __type: str
                x: float
                y: float
                z: float

            class MaxLinearAccelerationNegative2(BaseModel):
                __type: str
                x: float
                y: float
                z: float

            __type: str
            angularSpeed: float
            maxLinearAccelerationNegative: MaxLinearAccelerationNegative2
            maxLinearAccelerationPositive: MaxLinearAccelerationPositive2
            maxRotationAccel: float
            pidAggression: float

        boostPhase: BoostPhase
        boostPhaseDuration: float
        dumbfireRotationScale: float
        fuelTankSize: float
        interceptPhase: InterceptPhase
        isDumbMissile: bool
        linearSpeed: float
        pidDerivativeTerm: float
        pidIntegralTerm: float
        pidProportionalTerm: float
        terminalPhase: TerminalPhase
        terminalPhaseEngagementAngle: float
        terminalPhaseEngagementTime: float

    class ExplosionParams(BaseModel):
        class Damage(BaseModel):
            DamageBiochemical: float
            DamageDistortion: float
            DamageEnergy: float
            DamagePhysical: float
            DamageStun: float
            DamageThermal: float
            __polymorphicType: str
            __type: str

        __type: str
        angle: float
        angleVertical: float
        customMaterialEffect: str
        damage: Damage
        effectScale: float
        effectScaleMax: float
        effectScaleMin: float
        friendlyFire: str
        hitType: str
        holeSize: float
        maxPhysRadius: float
        maxRadius: float
        maxblurdist: float
        minPhysRadius: float
        minRadius: float
        particleStrength: float
        pressure: float
        radarContactType: str
        soundRadius: float
        terrainHoleSize: float
        useRandomScale: bool

    class TargetingParams(BaseModel):
        __type: str
        allowDumbFiring: bool
        dynamicLaunchZoneRecord: str
        lockDecreaseRate: float
        lockIncreaseRate: float
        lockRangeMax: float
        lockRangeMin: float
        lockResolutionRadius: float
        lockSignalAmplifier: float
        lockTime: float
        lockingAngle: float
        minRatioForLock: float
        signalResilienceMax: float
        signalResilienceMin: float
        trackingSignalMin: float
        trackingSignalType: str

    GCSParams: GCSParams
    armTime: float
    collisionDelayTime: float
    enableLifetime: bool
    explosionParams: ExplosionParams
    explosionSafetyDistance: float
    igniteTime: float
    maxLifetime: float
    projectileProximity: float
    requiresLauncher: bool
    targetingParams: TargetingParams

    def to_missile_info(self) -> MissileInfo:
        return MissileInfo(
            damage=UniversalData.Damage(
                damage_biochemical=self.explosionParams.damage.DamageBiochemical,
                damage_distortion=self.explosionParams.damage.DamageDistortion,
                damage_energy=self.explosionParams.damage.DamageEnergy,
                damage_physical=self.explosionParams.damage.DamagePhysical,
                damage_stun=self.explosionParams.damage.DamageStun,
                damage_thermal=self.explosionParams.damage.DamageThermal
            ),
            tracking_signal_type=self.targetingParams.trackingSignalType,
            speed=self.GCSParams.linearSpeed,
            arm_time=self.armTime,
            lock_angle=self.targetingParams.lockingAngle,
            lock_time=self.targetingParams.lockTime,
            lock_range_min=self.targetingParams.lockRangeMin,
            lock_range_max=self.targetingParams.lockRangeMax,
            ignite_time=self.igniteTime,
            explosion_radius_min=self.explosionParams.minRadius,
            explosion_radius_max=self.explosionParams.maxRadius
        )


class SItemPortContainerComponentParamsType(BaseModel):
    class Port(BaseModel):
        class SItemPortDef(BaseModel):

            AttachmentPoints: List
            Connections: List
            DefaultWeaponGroup: str
            DisabledPortLinks: List
            DisplayName: str
            Flags: str
            InteractionPointSize: float
            MaxSize: int
            MinSize: int
            Name: str
            PortTags: str
            RequiredPortTags: str
            Tags: List
            itemPortRules: List
            linkedItemPorts: List

        SItemPortDef: SItemPortDef

    InternalHardpointLinks: List
    InternalResourceLinks: List
    PortFlags: str
    PortTags: str
    Ports: List[Port]
    RequiredItemTags: str