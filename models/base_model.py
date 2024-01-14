from pydantic import BaseModel
from typing import List, Optional


class UniversalData(BaseModel):
    type: str
    name: str
    chinese_name: Optional[str]
    description: Optional[str] = None
    chinese_description: Optional[str] = None
    ref: str


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


class SCItemWeaponComponentParams(BaseModel):
    class WeaponRegenConsumerParams(BaseModel):
        __type: str
        regenerationCooldown: float
        regenerationCostPerBullet: float
        requestedAmmoLoad: float
        requestedRegenPerSec: float

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


class SAmmoContainerComponentParams(BaseModel):
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