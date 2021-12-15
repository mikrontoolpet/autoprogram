from pathlib import Path
import math
import asyncio
from autoprogram.tools.common import BaseTool
from autoprogram.wbhandler import WorkBook

DEC_DIGITS = 3

class Tool(BaseTool):
    """
    CrazyDrill Cool SST-Inox (IC) drill class
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/drills/ic"

    def __init__(self, vgp_client, name, diam, fl_len, lead=None):
        super().__init__(vgp_client, name, Tool.family_address) # update class name here too!
        self.diam = float(diam)
        self.fl_len = float(fl_len)
        self.configuration_wb = WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/ic/worksheets/configuration_file.xlsx")
        self.diam_lt_3 = self.diam < 3

        # Set the lead depending on whether it is a user input or from table
        if lead is None:
            self.lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        else:
            self.lead = float(lead)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6.35)
        self.check_boundary(self.fl_len, 6*self.diam, 17.999*self.diam)

    async def set_parameters(self):

        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")

        # Blank
        # Profile
        conic_len = 4.25*self.diam
        conic_len_p4 = conic_len + end_stk_rmv
        back_taper = 200
        neck_diam = round(self.diam - conic_len*(1/back_taper), DEC_DIGITS)
        fillet_rad = round(0.5*self.diam, DEC_DIGITS)
        shank_diam = self.configuration_wb.lookup("blank", "diameter", self.diam, "shank_diameter")
        tang_len = self.fl_len + 0.1*self.diam + end_stk_rmv
        tot_len = self.configuration_wb.lookup("blank", "diameter", self.diam, "tot_len_6_14xd") + end_stk_rmv

        await self.vgpc.set("ns=2;s=tool/Blank/Profile/Diameter", self.diam)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/Diameter neck", neck_diam)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/Diameter shank", shank_diam)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/Length tangent", tang_len)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/Radius", fillet_rad)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/Length total", tot_len)

        # Coolant holes
        # Group 1
        hole_cent_rad_1 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_1")
        hole_diam_1 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_1")

        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Helicoidal Holes/Helicoidal Holes/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Distance from center", hole_cent_rad_1)
        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Holes Diameter", hole_diam_1)

        # Group 2
        hole_cent_rad_2 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_2")
        hole_diam_2 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_2")

        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Helicoidal Holes/Helicoidal Holes/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Distance from center", hole_cent_rad_2)
        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Holes Diameter", hole_diam_2)

        # Group 3
        hole_cent_rad_3 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_3")
        hole_diam_3 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_3")

        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Helicoidal Holes/Helicoidal Holes/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Distance from center", hole_cent_rad_3)
        await self.vgpc.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Holes Diameter", hole_diam_3)


        # Set parameters

        # Common Data
        fl_stk_rmv = min([0.08, 0.025*self.diam])
        d700 = self.common_wb.lookup("D700", "diameter", self.diam, "D700")
        await self.vgpc.set("ns=2;s=tool/Tool/Reference Length (RL)", 1.5*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/End Stock Removal (dL)", end_stk_rmv)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", d700)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Cutting Security Distance", d700)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Cutting Security Distance", d700)

        # Set 1
        # Profile
        point_ang = 141
        point_len = (self.diam/2)/math.tan(math.radians(point_ang/2))
        ta0 = 0
        sp1_len = 4.35*self.diam - point_len + 0.13*self.diam
        strgh_diam = 1
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", point_ang)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", ta0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", sp1_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Straightness Diameter", strgh_diam)

        # Flute 1
        front_dl_start = 0.2
        front_fl_len = 3.3*self.diam
        back_fl_len = self.fl_len - front_fl_len
        fl_len_end_diff = 0.275*self.diam

        if self.diam_lt_3:
            fl_1_len = self.fl_len
        else:
            fl_1_len = front_fl_len

        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", fl_1_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G1)
        g1_core_diam = 30
        g1_end_diff = self.configuration_wb.trend("function_data", "diameter", self.diam, "G1_end_diff")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", front_dl_start)
        if self.diam_lt_3:
            g1_dl_end = -back_fl_len + g1_end_diff
        else:
            g1_dl_end = g1_end_diff
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL End", g1_dl_end)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Infeed Down Y", 0.15*self.diam)
        # Feeds and speeds
        g1_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_speed")
        g1_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (G2)
        g2_rake_shift = self.configuration_wb.trend("function_data", "diameter", self.diam, "G2_rake_shift")
        g2_end_diff = self.configuration_wb.trend("function_data", "diameter", self.diam, "G2_end_diff")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", g2_rake_shift)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL Start", front_dl_start)
        if self.diam_lt_3:
            g2_dl_end = -back_fl_len + g2_end_diff
        else:
            g2_dl_end = g2_end_diff
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", g2_dl_end)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", 0.15*self.diam)
        # Feeds and speeds
        g2_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_speed")
        g2_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Cutting Speed", g2_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate", g2_feedrate)

        # Flute 201 (S_G1)
        # If Ø is less than 3 mm, S_G1 and S_G3 are performed with a single
        # pass of S_G1
        s_g1_core_diam = g1_core_diam + 2*fl_stk_rmv/self.diam*100
        s_g1_att_ang = self.configuration_wb.trend("function_data", "diameter", self.diam, "S_G1_attack_angle")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", -fl_stk_rmv)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Core Diameter", s_g1_core_diam) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Attack Angle", s_g1_att_ang) # FROM TABLE
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL Start", front_dl_start)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL End", -fl_len_end_diff)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Infeed Down Y", 0.15*self.diam)

        # If S_G1 is roughing the whole flute, needs an exit radius
        if self.diam_lt_3:
            sg1_exit_radius = 0.5*self.diam
            s_g1_dl_end = -fl_len_end_diff
        else:
            sg1_exit_radius = 0
            s_g1_dl_end = self.configuration_wb.trend("function_data", "diameter", self.diam, "S_G1_dl_end")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL End", s_g1_dl_end)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Exit Radius", sg1_exit_radius)

        # Feeds and speeds
        # MISSING DATA!!!

        # Step 0
        sc = 0.008*self.diam
        s1_rake = 2
        tn3_rake = -10
        tn3_width = self.configuration_wb.lookup("tn_width", "diameter", self.diam, "tn_width")
        s1_offset = tn3_width*(math.tan(math.radians(s1_rake)) + math.tan(math.radians(-tn3_rake)))
        s1_web_thck = sc + s1_offset
        # Gash 1 (S1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Web Thickness", s1_web_thck)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Rake Angle", s1_rake)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Depth Past Center Yp", -0.02429*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Profile 2D/sR", 0.0649*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Profile 2D/sL", 0.55*self.diam)

        # Gash 101 (TN3)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Web Thickness", sc)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Rake Angle", tn3_rake)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Depth Past Center Yp", -0.03*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Profile 2D/sR", 0.0649*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Profile 2D/sL", 0.0786*self.diam)

        # Gash 201 (TN1)
        tn1_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN1_gash_rotation")
        tn1_web_thck = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN1_web_thickness")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Gash Rotation", tn1_index)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Web Thickness", tn1_web_thck)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Depth Past Center Yp", -0.2*self.diam)

        # Point Relief
        # Relief 1
        # Point Relief 1 (P1)
        pass
        # Point Relief 2 (P2)
        pass
        # Relief 101
        # Point Relief 102 (S_P2)
        pass

        # Step 0 Diameter
        # Step 0 OD Clearance
        # OD Clearance 1 (F1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", 0.0857*self.diam)

        # OD Clearance 101 (F2)
        f2_marg_width = self.configuration_wb.trend("function_data", "diameter", self.diam, "F2_margin_width")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", f2_marg_width)

        # Set 2
        # Profile
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Profile/pA", point_ang)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Profile/D0", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Profile/Ta0", ta0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Profile/sP1", sp1_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Straightness Diameter", strgh_diam)

        # Flute 1
        back_flutes_dz = -front_fl_len
        back_flutes_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "Back_Flutes_index")
        back_flutes_len = back_flutes_dz + self.fl_len
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Index", back_flutes_index)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Custom Profile Flute/dZ", back_flutes_dz)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Custom Profile Flute/D", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Custom Profile Flute/L", back_flutes_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G3)
        g3_core_diam = 25
        g3_dl_start = self.configuration_wb.trend("function_data", "diameter", self.diam, "G3_dl_start")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", g3_core_diam) # in %
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", g3_dl_start)  
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL End", -fl_len_end_diff)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Infeed Down Y", 0.2*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Flute 101 (S_G3)
        # If Ø is less than 3 mm, S_G1 and S_G3 are performed with a single
        # pass of S_G1
        if not self.diam_lt_3:
            s_g3_core_diam = g3_core_diam + 2*fl_stk_rmv/self.diam*100
            s_g3_att_ang = self.configuration_wb.trend("function_data", "diameter", self.diam, "S_G3_attack_angle")
            s_g3_dl_start = self.configuration_wb.trend("function_data", "diameter", self.diam, "S_G3_dl_start")
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", -fl_stk_rmv)
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", s_g3_core_diam) # in %
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Attack Angle", s_g3_att_ang)
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/dL Start", s_g3_dl_start)
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/dL End", -fl_len_end_diff)
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", 0.2*self.diam)
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Exit Radius", 0.5*self.diam)
            # Feeds and speeds
            # MISSING DATA!!!
        else:
            pass

        # Flute 201 (RN1)
        rn_1_rake_shift = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN1_rake_shift")
        rn1_dl_start = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN1_dl_start")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", rn_1_rake_shift)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/dL Start", rn1_dl_start)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/dL End", -0.8*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Infeed Down Y", 0.2*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Flute 301 (RN2)
        rn2_dl_start = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN2_dl_start")
        rn_2_rake_shift = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN2_rake_shift")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Rake Shift", rn_2_rake_shift)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/dL Start", rn2_dl_start)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/dL End", -0.8*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Infeed Down Y", 0.15*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Infeed Motion (Start)/Z", 0.01429*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Infeed Motion (Start)/Y", 0.25*self.diam)
        # await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Security Distance (End)", 0.25*self.diam)
        # Feeds and speeds
        # MISSING DATA!!!

        # Set 3
        tn2_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN2_index")
        tn2_web_thck = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN2_web_thickness")
        tn2_sr = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN2_sR")
        # OD Profile 2D
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Diameter", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Distance", 0.3*self.diam)
        # Gash 1 (TN2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Index", tn2_index) # FROM TABLE
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/D", 1.17*self.diam) # FROM TABLE
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/dD", 0.943*self.diam) # FROM TABLE
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/dZ", -0.168*self.diam) # FROM TABLE
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Web Thickness", tn2_web_thck) # FROM TABLE
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Profile 2D/sR", tn2_sr) # FROM TABLE
        # Relief 1 (SM)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Reliefs/Relief Section 1/Relief 1/Cam 1/Exit distance", 0.2*self.diam)

    async def set_wheels(self):
        """
        Load wheelpacks and set wheel segments
        """
        # Load wheelpack 1
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_1")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 1)
        # Load wheelpack 2
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_2")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 2)
        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpack_6", "diameter", self.diam, "wheelpack_6")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 6)

        # Set wheel segments for wheelpack 1
        # S_G1
        op_wh_seg = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)

        # S_G3 (only if diameter >= 3)
        if self.diam_lt_3:
            pass
        else:
            op_wh_seg = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G3_wheel")
            await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)
        # RN1
        op_wh_seg = self.configuration_wb.lookup("rn", "diameter", self.diam, "RN12_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)
        # RN2
        op_wh_seg = self.configuration_wb.lookup("rn", "diameter", self.diam, "RN12_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Wheel", op_wh_seg)
        # F1
        op_wh_seg = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Wheel", op_wh_seg)
        # F2
        op_wh_seg = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 2
        # S1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "S1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Wheel", op_wh_seg)
        # TN1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Wheel", op_wh_seg)
        # TN2
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Wheel", op_wh_seg)
        # TN3
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN3_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Wheel", op_wh_seg)
        # P1
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
        # P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
        # S_P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)
        # SM
        op_wh_seg = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 6
        # G1
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
        # G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)
        # G3
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G3_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)

    async def set_isoeasy(self):
        """
        Load specified isoeasy program
        """
        isoeasy_raw_path = self.configuration_wb.lookup("isoeasy", "diameter", self.diam, "isoeasy_raw_path")
        await self.vgpc.load_isoeasy(isoeasy_raw_path)