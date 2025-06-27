
bl_info = {
    "name": "SL to VRM Converter (Complete Toolkit)",
    "author": "The Mighty Ginkgo and ChatGPT",
    "version": (1, 9),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > SL to VRM",
    "description": "SL to VRM converter with dual rotation buttons and bone X-ray toggle",
    "category": "Rigging",
}

import bpy
import math

sl_to_vrm_map = {
    "mPelvis": "J_Bip_C_Hips", "mTorso": "J_Bip_C_Spine", "mChest": "J_Bip_C_Chest", "mNeck": "J_Bip_C_Neck",
    "mHead": "J_Bip_C_Head", "mCollarLeft": "J_Bip_L_Shoulder", "mShoulderLeft": "J_Bip_L_UpperArm",
    "mElbowLeft": "J_Bip_L_LowerArm", "mWristLeft": "J_Bip_L_Hand", "mCollarRight": "J_Bip_R_Shoulder",
    "mShoulderRight": "J_Bip_R_UpperArm", "mElbowRight": "J_Bip_R_LowerArm", "mWristRight": "J_Bip_R_Hand",
    "mHipLeft": "J_Bip_L_UpperLeg", "mKneeLeft": "J_Bip_L_LowerLeg", "mAnkleLeft": "J_Bip_L_Foot",
    "mFootLeft": "J_Bip_L_ToeBase", "mHipRight": "J_Bip_R_UpperLeg", "mKneeRight": "J_Bip_R_LowerLeg",
    "mAnkleRight": "J_Bip_R_Foot", "mFootRight": "J_Bip_R_ToeBase", "mEyeLeft": "J_Adj_L_FaceEye",
    "mEyeRight": "J_Adj_R_FaceEye", "Tail Base": "J_Opt_C_CatTail1_01", "mTail1": "J_Opt_C_CatTail2_01",
    "mTail2": "J_Opt_C_CatTail3_01", "mTail3": "J_Opt_C_CatTail4_01", "mTail4": "J_Opt_C_CatTail5_01",
    "mTail5": "J_Opt_C_CatTail6_01", "mTail6": "J_Opt_C_CatTail8_01", "Left Ear": "J_Opt_L_CatEar1_01",
    "mFaceEar1Left": "J_Opt_L_CatEar2_01", "mFaceEar2Left": "J_Opt_L_CatEar2_end_01",
    "Right Ear": "J_Opt_R_CatEar1_01", "mFaceEar1Right": "J_Opt_R_CatEar2_01",
    "mFaceEar2Right": "J_Opt_R_CatEar2_end_01"
,
    "mHandThumb1Left": "J_Bip_L_Thumb1",
    "mHandThumb2Left": "J_Bip_L_Thumb2",
    "mHandThumb3Left": "J_Bip_L_Thumb3",
    "mHandIndex1Left": "J_Bip_L_Index1",
    "mHandIndex2Left": "J_Bip_L_Index2",
    "mHandIndex3Left": "J_Bip_L_Index3",
    "mHandMiddle1Left": "J_Bip_L_Middle1",
    "mHandMiddle2Left": "J_Bip_L_Middle2",
    "mHandMiddle3Left": "J_Bip_L_Middle3",
    "mHandRing1Left": "J_Bip_L_Ring1",
    "mHandRing2Left": "J_Bip_L_Ring2",
    "mHandRing3Left": "J_Bip_L_Ring3",
    "mHandPinky1Left": "J_Bip_L_Little1",
    "mHandPinky2Left": "J_Bip_L_Little2",
    "mHandPinky3Left": "J_Bip_L_Little3",
    "mHandThumb1Right": "J_Bip_R_Thumb1",
    "mHandThumb2Right": "J_Bip_R_Thumb2",
    "mHandThumb3Right": "J_Bip_R_Thumb3",
    "mHandIndex1Right": "J_Bip_R_Index1",
    "mHandIndex2Right": "J_Bip_R_Index2",
    "mHandIndex3Right": "J_Bip_R_Index3",
    "mHandMiddle1Right": "J_Bip_R_Middle1",
    "mHandMiddle2Right": "J_Bip_R_Middle2",
    "mHandMiddle3Right": "J_Bip_R_Middle3",
    "mHandRing1Right": "J_Bip_R_Ring1",
    "mHandRing2Right": "J_Bip_R_Ring2",
    "mHandRing3Right": "J_Bip_R_Ring3",
    "mHandPinky1Right": "J_Bip_R_Little1",
    "mHandPinky2Right": "J_Bip_R_Little2",
    "mHandPinky3Right": "J_Bip_R_Little3"}

vrm_humanoid_map = {
    "hips": "J_Bip_C_Hips", "spine": "J_Bip_C_Spine", "chest": "J_Bip_C_Chest", "neck": "J_Bip_C_Neck",
    "head": "J_Bip_C_Head", "leftShoulder": "J_Bip_L_Shoulder", "leftUpperArm": "J_Bip_L_UpperArm",
    "leftLowerArm": "J_Bip_L_LowerArm", "leftHand": "J_Bip_L_Hand", "rightShoulder": "J_Bip_R_Shoulder",
    "rightUpperArm": "J_Bip_R_UpperArm", "rightLowerArm": "J_Bip_R_LowerArm", "rightHand": "J_Bip_R_Hand",
    "leftUpperLeg": "J_Bip_L_UpperLeg", "leftLowerLeg": "J_Bip_L_LowerLeg", "leftFoot": "J_Bip_L_Foot",
    "leftToes": "J_Bip_L_ToeBase", "rightUpperLeg": "J_Bip_R_UpperLeg", "rightLowerLeg": "J_Bip_R_LowerLeg",
    "rightFoot": "J_Bip_R_Foot", "rightToes": "J_Bip_R_ToeBase", "leftEye": "J_Adj_L_FaceEye", "rightEye": "J_Adj_R_FaceEye"
,
    "leftThumbProximal": "J_Bip_L_Thumb1",
    "leftThumbIntermediate": "J_Bip_L_Thumb2",
    "leftThumbDistal": "J_Bip_L_Thumb3",
    "leftIndexProximal": "J_Bip_L_Index1",
    "leftIndexIntermediate": "J_Bip_L_Index2",
    "leftIndexDistal": "J_Bip_L_Index3",
    "leftMiddleProximal": "J_Bip_L_Middle1",
    "leftMiddleIntermediate": "J_Bip_L_Middle2",
    "leftMiddleDistal": "J_Bip_L_Middle3",
    "leftRingProximal": "J_Bip_L_Ring1",
    "leftRingIntermediate": "J_Bip_L_Ring2",
    "leftRingDistal": "J_Bip_L_Ring3",
    "leftLittleProximal": "J_Bip_L_Little1",
    "leftLittleIntermediate": "J_Bip_L_Little2",
    "leftLittleDistal": "J_Bip_L_Little3",
    "rightThumbProximal": "J_Bip_R_Thumb1",
    "rightThumbIntermediate": "J_Bip_R_Thumb2",
    "rightThumbDistal": "J_Bip_R_Thumb3",
    "rightIndexProximal": "J_Bip_R_Index1",
    "rightIndexIntermediate": "J_Bip_R_Index2",
    "rightIndexDistal": "J_Bip_R_Index3",
    "rightMiddleProximal": "J_Bip_R_Middle1",
    "rightMiddleIntermediate": "J_Bip_R_Middle2",
    "rightMiddleDistal": "J_Bip_R_Middle3",
    "rightRingProximal": "J_Bip_R_Ring1",
    "rightRingIntermediate": "J_Bip_R_Ring2",
    "rightRingDistal": "J_Bip_R_Ring3",
    "rightLittleProximal": "J_Bip_R_Little1",
    "rightLittleIntermediate": "J_Bip_R_Little2",
    "rightLittleDistal": "J_Bip_R_Little3"}

class SL2VRM_OT_ConvertFull(bpy.types.Operator):
    bl_idname = "object.sl_to_vrm_convert"
    bl_label = "Convert SL Skeleton to VRM"
    def execute(self, context):
        obj = context.object
        if not obj or obj.type != "ARMATURE":
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        renamed = 0
        renamed_bones = {}
        skipped_bones = []

        for sl, vrm in sl_to_vrm_map.items():
            if sl in obj.data.edit_bones:
                obj.data.edit_bones[sl].name = vrm
                renamed_bones[sl] = vrm
                renamed += 1
            else:
                skipped_bones.append(sl)

        bpy.ops.object.mode_set(mode='OBJECT')

        for mesh_obj in bpy.data.objects:
            if mesh_obj.type == 'MESH':
                for mod in mesh_obj.modifiers:
                    if mod.type == 'ARMATURE' and mod.object == obj:
                        for sl_name, vrm_name in renamed_bones.items():
                            if sl_name in mesh_obj.vertex_groups:
                                vg = mesh_obj.vertex_groups.get(sl_name)
                                vg.name = vrm_name


        self.report({'INFO'}, f"Renamed bones: {renamed}, Skipped bones: {len(skipped_bones)}")
        print("=== SL to VRM Conversion Debug ===")
        print("Renamed Bones:")
        for sl, vrm in renamed_bones.items():
            print(f"  {sl} -> {vrm}")
        if skipped_bones:
            print("Skipped Bones (not found in armature):")
            for sl in skipped_bones:
                print(f"  {sl}")
        print("==================================")

        ext = obj.data.vrm_addon_extension
        ext.vrm0.meta.title = "Converted VRM"
        ext.vrm0.meta.author = "The Mighty Ginkgo"
        ext.vrm0.meta.version = "1.0"


        human = ext.vrm0.humanoid
        pose_bones = obj.pose.bones

        # Keep track of what was added and what was skipped
        added_bones = []
        skipped_bones = []

        # Clear old slots that match our map keys
        existing_keys = set([hb.bone for hb in human.human_bones])
        for slot in vrm_humanoid_map:
            if slot in existing_keys:
                for i, hb in enumerate(human.human_bones):
                    if hb.bone == slot:
                        human.human_bones.remove(i)
                        break

        # Assign new bones only if they exist in pose.bones
        for slot, bone in vrm_humanoid_map.items():
            if bone in pose_bones:
                b = human.human_bones.add()
                b.bone = slot
                b.node.value = bone
                added_bones.append((slot, bone))
            else:
                skipped_bones.append((slot, bone))

        print("=== VRM Humanoid Bone Assignment ===")
        print("✔️ Added Bones:")
        for slot, bone in added_bones:
            print(f"  {slot} -> {bone}")
        if skipped_bones:
            print("❌ Skipped Bones (not found in pose.bones):")
            for slot, bone in skipped_bones:
                print(f"  {slot} -> {bone}")
        print("====================================")

        missing_bones = []
        for slot, bone in vrm_humanoid_map.items():
            if bone in obj.pose.bones:
                b = human.human_bones.add()
                b.bone = slot
                b.node.value = bone
            else:
                missing_bones.append((slot, bone))
        if missing_bones:
            self.report({'WARNING'}, f"Some bones could not be assigned: {missing_bones}")

        self.report({'INFO'}, f"{renamed} bones renamed and vertex groups updated.")
        return {'FINISHED'}

class SL2VRM_OT_RebindArmatureModifiers(bpy.types.Operator):
    bl_idname = "object.sl_to_vrm_rebind_modifiers"
    bl_label = "Refresh Armature Modifier"
    def execute(self, context):
        armature = context.object
        if not armature or armature.type != "ARMATURE":
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        rebounded = 0
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for mod in obj.modifiers:
                    if mod.type == 'ARMATURE' and mod.object == armature:
                        mod.object = None
                        mod.object = armature
                        rebounded += 1

        self.report({'INFO'}, f"{rebounded} mesh object(s) rebound to armature.")
        return {'FINISHED'}

class SL2VRM_OT_TurnAroundMinus90(bpy.types.Operator):
    bl_idname = "object.sl_to_vrm_turn_minus"
    bl_label = "Turn Around (-90° Z)"
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in bpy.context.view_layer.objects:
            if obj.visible_get():
                obj.select_set(True)
        bpy.ops.transform.rotate(value=-math.radians(90), orient_axis='Z')
        return {'FINISHED'}

class SL2VRM_OT_TurnAroundPlus90(bpy.types.Operator):
    bl_idname = "object.sl_to_vrm_turn_plus"
    bl_label = "Turn Around (+90° Z)"
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in bpy.context.view_layer.objects:
            if obj.visible_get():
                obj.select_set(True)
        bpy.ops.transform.rotate(value=math.radians(90), orient_axis='Z')
        return {'FINISHED'}

class SL2VRM_OT_ToggleXRay(bpy.types.Operator):
    bl_idname = "object.sl_to_vrm_xray_toggle"
    bl_label = "Toggle X-Ray for Bones"
    def execute(self, context):
        arm = context.object
        if not arm or arm.type != "ARMATURE":
            self.report({'ERROR'}, "Select armature")
            return {'CANCELLED'}
        arm.show_in_front = not arm.show_in_front
        return {'FINISHED'}

class SL2VRM_PT_Tools(bpy.types.Panel):
    bl_label = "SL to VRM Tools"
    bl_idname = "VIEW3D_PT_sl2vrm_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SL to VRM'
    def draw(self, context):
        self.layout.operator("object.sl_to_vrm_convert", icon="ARMATURE_DATA")
        self.layout.operator("object.sl_to_vrm_turn_minus", icon="TRIA_LEFT")
        self.layout.operator("object.sl_to_vrm_turn_plus", icon="TRIA_RIGHT")
        self.layout.operator("object.sl_to_vrm_xray_toggle", icon="HIDE_OFF")
        self.layout.operator("object.sl_to_vrm_rebind_modifiers", text="Refresh Armature Modifier", icon="FILE_REFRESH")

def register():
    bpy.utils.register_class(SL2VRM_OT_ConvertFull)
    bpy.utils.register_class(SL2VRM_OT_TurnAroundMinus90)
    bpy.utils.register_class(SL2VRM_OT_TurnAroundPlus90)
    bpy.utils.register_class(SL2VRM_OT_ToggleXRay)
    bpy.utils.register_class(SL2VRM_OT_RebindArmatureModifiers)
    bpy.utils.register_class(SL2VRM_PT_Tools)

def unregister():
    bpy.utils.unregister_class(SL2VRM_OT_ConvertFull)
    bpy.utils.unregister_class(SL2VRM_OT_TurnAroundMinus90)
    bpy.utils.unregister_class(SL2VRM_OT_TurnAroundPlus90)
    bpy.utils.unregister_class(SL2VRM_OT_ToggleXRay)
    bpy.utils.unregister_class(SL2VRM_OT_RebindArmatureModifiers)
    bpy.utils.unregister_class(SL2VRM_PT_Tools)

if __name__ == "__main__":
    register()
