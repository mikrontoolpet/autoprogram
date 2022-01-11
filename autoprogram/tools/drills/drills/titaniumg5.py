from pathlib import Path
import math
from autoprogram.tools.common import BaseTool
from autoprogram.wbhandler import WorkBook

class Tool(BaseTool):
    """
    CrazyDrill Titanium Grade 5 (ATC) drill class
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/drills/titaniumg5"

    def __init__(self, vgp_client, name, diam, fl_len, lead=None):
        super().__init__(vgp_client, name, Tool.family_address) # update class name here too!
        self.diam = float(diam)
        self.fl_len = float(fl_len)
        self.configuration_wb = WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/titaniumg5/worksheets/configuration_file.xlsx")

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
        # # Profile
        # conic_len = 4.25*self.diam
        # conic_len_p4 = conic_len + end_stk_rmv
        # back_taper = 200
        # neck_diam = self.diam - conic_len*(1/back_taper)
        # fillet_rad = 0.1# round(0.5*self.diam, DEC_DIGITS)
        # shank_diam = self.configuration_wb.lookup("blank", "diameter", self.diam, "shank_diameter")
        # tang_len = self.fl_len + 0.1*self.diam + end_stk_rmv
        tot_len = self.configuration_wb.lookup("blank", "diameter", self.diam, "tot_len")

        await self.vgpc.set("ns=2;s=tool/Blank/Profile/D", self.diam)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/L", tot_len)
        # await self.vgpc.set("ns=2;s=tool/Blank/Profile/Diameter", self.diam)
        # await self.vgpc.set("ns=2;s=tool/Blank/Profile/Diameter neck", neck_diam)
        # await self.vgpc.set("ns=2;s=tool/Blank/Profile/Diameter shank", shank_diam)
        # await self.vgpc.set("ns=2;s=tool/Blank/Profile/Length tangent", tang_len)
        # await self.vgpc.set("ns=2;s=tool/Blank/Profile/Radius", fillet_rad)
        # await self.vgpc.set("ns=2;s=tool/Blank/Profile/Length total", tot_len)

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
        # Set 1
        # Common Data
        d700 = self.common_wb.lookup("D700", "diameter", self.diam, "D700")
        await self.vgpc.set("ns=2;s=tool/Tool/Reference Length (RL)", 1.5*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/End Stock Removal (dL)", end_stk_rmv)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", d700)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Cutting Security Distance", d700)

       # Set 1
        # Profile
        point_ang = 140
        point_len = (self.diam/2)/math.tan(math.radians(point_ang/2))
        ta0 = -0.0286
        sp1_len = self.fl_len - 1.4*self.diam - point_len
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", point_ang)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", ta0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", sp1_len)

        # Flute 1
        front_dl_start = 0.2
        fl_len_end_diff = -0.07375*self.diam
        fl_1_len = self.fl_len
        infeed_down_y = 0.04*self.diam + 0.06
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", fl_1_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G1)
        # Core diameter, rake angle and circular land width have a transition in values along the flute length
        g1_trans_len = 5*self.diam
        g1_len = fl_1_len
        g1_trans_perc = (g1_trans_len - point_len)/(g1_len - point_len)*100
        g1_core_diam_perc_1 = 32
        g1_core_diam_perc_2 = 27
        g1_rake_ang_1 = 16
        g1_rake_ang_2 = 19
        g1_circ_land_width_1 = 0.8*self.diam
        g1_circ_land_width_2 = 0.75*self.diam
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", "(s1;0%;" + str(g1_core_diam_perc_1) + "%);(s1;" + str(g1_trans_perc) + "%;" + str(g1_core_diam_perc_2) + "%);(s1;100%;" + str(g1_core_diam_perc_2) + "%)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Rake Angle", "(s1;0%;" + str(g1_rake_ang_1) + "°);(s1;" + str(g1_trans_perc) + "%;" + str(g1_rake_ang_2) + "°);(s1;100%;" + str(g1_rake_ang_2) + "°)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", "(s1;0%;" + str(g1_circ_land_width_1) + " mm);(s1;" + str(g1_trans_perc) + ";" + str(g1_circ_land_width_2) + " mm);(s1;100%;" + str(g1_circ_land_width_2) + " mm)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", front_dl_start)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL End", -0.5*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Exit Radius", 0.25*self.diam)
        # Feeds and speeds
        g1_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_speed")
        g1_feedrate_in = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate_in")
        g1_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate In", g1_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (S_G1)
        """
        Roughing flute has 2 stock removals:
        - one for the rake
        - one for the core
        """
        # Rake radial stock removal
        s_g1_rake_rad_stk_rmv = 0.008*self.diam + 0.012
        # Core radial stock removal
        s_g1_core_rad_stk_rmv = (0.0278 - 0.00278*self.diam)*self.diam
        s_g1_core_rad_stk_rmv_perc = s_g1_core_rad_stk_rmv/self.diam*100 # radial stock removal percentage
        s_g1_core_stk_rmv_perc = 2*s_g1_core_rad_stk_rmv_perc # total stock removal percentage

        s_g1_trans_perc = g1_trans_perc
        s_g1_core_diam_perc_1 = g1_core_diam_perc_1 + s_g1_core_stk_rmv_perc
        s_g1_core_diam_perc_2 = g1_core_diam_perc_2 + s_g1_core_stk_rmv_perc
        s_g1_rake_ang_diff = -2 # roughing flute has a rake angle 2° less than the polishing
        s_g1_rake_ang_1 = g1_rake_ang_1 + s_g1_rake_ang_diff
        s_g1_rake_ang_2 = g1_rake_ang_2 + s_g1_rake_ang_diff
        # Roughing land width is increased by the same amount of the core stock removal
        s_g1_circ_land_width_1 = g1_circ_land_width_1 + s_g1_core_rad_stk_rmv
        s_g1_circ_land_width_2 = g1_circ_land_width_2 + s_g1_core_rad_stk_rmv
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", -s_g1_rake_rad_stk_rmv)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", "(s1;0%;" + str(s_g1_core_diam_perc_1) + "%);(s1;" + str(s_g1_trans_perc) + "%;" + str(s_g1_core_diam_perc_2) + "%);(s1;100%;" + str(s_g1_core_diam_perc_2) + "%)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Angle", "(s1;0%;" + str(s_g1_rake_ang_1) + "°);(s1;" + str(s_g1_trans_perc) + "%;" + str(s_g1_rake_ang_2) + "°);(s1;100%;" + str(s_g1_rake_ang_2) + "°)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Circular Land Width", "(s1;0%;" + str(s_g1_circ_land_width_1) + " mm);(s1;" + str(s_g1_trans_perc) + "%;" + str(s_g1_circ_land_width_2) + " mm);(s1;100%;" + str(s_g1_circ_land_width_2) + " mm)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL Start", front_dl_start)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", fl_len_end_diff)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Exit Radius", 0.25*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", infeed_down_y)
        # Feeds and speeds
        s_g1_speed = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_speed")
        s_g1_feedrate_in = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_feedrate_in")
        s_g1_feedrate = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Cutting Speed", s_g1_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate In", s_g1_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate", s_g1_feedrate)

        # Flute 201 (RN)
        rn_nom_dl_start = -5*self.diam
        rn_dl_start_diff = -0.033*self.diam
        rn_dl_start = rn_nom_dl_start + rn_dl_start_diff
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", 0.0166*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL Start", rn_dl_start)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL End", -self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Exit Radius", 0.1*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Infeed Down Y", infeed_down_y)
        # Feeds and speeds
        rn_speed = self.configuration_wb.lookup("RN", "diameter", self.diam, "RN_speed")
        rn_feedrate_in = self.configuration_wb.lookup("RN", "diameter", self.diam, "RN_feedrate_in")
        rn_feedrate = self.configuration_wb.lookup("RN", "diameter", self.diam, "RN_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Cutting Speed", rn_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Feedrate In", rn_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Feedrate", rn_feedrate)

        # Flute 301 (ERF)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/dL Start", -2.5*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Infeed Down Y", 0.5*self.diam)
        # Feeds and speeds
        erf_speed = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_speed")
        erf_feedrate_in = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_feedrate_in")
        erf_feedrate = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Cutting Speed", erf_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Feedrate In", erf_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Feedrate", erf_feedrate)

        # Flute 1001 (G2)
        fl_1001_len = 5*self.diam
        fl_1001_dl_end = 0.5*self.diam
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", fl_1001_len)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", 1.03*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL Start", front_dl_start)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL End", fl_1001_dl_end)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Exit Radius", 0.1*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Infeed Down Y", infeed_down_y)
        # Feeds and speeds
        g2_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_speed")
        g2_feedrate_in = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate_in")
        g2_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Cutting Speed", g2_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Feedrate In", g2_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Feedrate", g2_feedrate)

        # Step 0
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance", 0.085*self.diam)
        # Gash (TN1)
        tn1_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN1_index")
        tn1_web_thick = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN1_web_thickness")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", tn1_index)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", tn1_web_thick)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)
        # Feeds and speeds
        tn1_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_speed")
        tn1_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate_in")
        tn1_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Cutting Speed", tn1_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Feedrate In", tn1_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Feed along sweep+exit", tn1_feedrate)

        # # S-Gash (SS)
        ss_yp = self.configuration_wb.trend("function_data", "diameter", self.diam, "SS_yp")
        ss_exit_ang_corr = self.configuration_wb.trend("function_data", "diameter", self.diam, "SS_exit_ang_corr")
        ss_chisel_dist_corr = self.configuration_wb.trend("function_data", "diameter", self.diam, "SS_chisel_dist_corr")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Web Thickness", -0.009*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", ss_yp)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.175*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle Correction", ss_exit_ang_corr)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Chisel Distance Correction", ss_chisel_dist_corr)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.0866*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.17*self.diam)
        # Feeds and speeds
        ss_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_speed")
        ss_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate_in")
        ss_feedrate_rotation = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate_rotation")
        ss_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Cutting Speed", ss_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feedrate In", ss_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feedrate", ss_feedrate_rotation)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feed along sweep", ss_feedrate)

        # Point Relief
        # Relief 1
        # Point Relief 1 (P1)
        # Feeds and speeds
        p1_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_speed")
        p1_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_feedrate_in")
        p1_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Cutting Speed", p1_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Feedrate In", p1_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Feedrate", p1_feedrate)
        # Point Relief 2 (P2)
        # Feeds and speeds
        p2_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_speed")
        p2_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_feedrate_in")
        p2_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Cutting Speed", p2_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Feedrate In", p2_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Feedrate", p2_feedrate)
        # Relief 101
        # Point Relief 102 (S_P2)
        # Feeds and speeds
        s_p2_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_speed")
        s_p2_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate_in")
        s_p2_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Cutting Speed", s_p2_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate In", s_p2_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate", s_p2_feedrate)

        # Step 0 Diameter
        # Step 0 OD Clearance
        # OD Clearance 1 (F1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Margin Width", 0.095*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Drop Angle", 3)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/dL Start", front_dl_start)
        # Feeds and speeds
        f1_speed = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_speed")
        f1_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Cutting Speed", f1_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate", f1_feedrate)

        # Set 2
        # OD Profile 2D
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter_Drill", self.diam)

        # Gash 1 (No)
        af_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "AF_index")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Index", af_index)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/D", self.diam)

        # Relief 1 (AF)
        af_dl = 0.0467*self.diam + 0.1033
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/dL Start", af_dl)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/dL End", af_dl)
        # Feeds and speeds
        af_speed = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_speed")
        af_feedrate_in = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_feedrate_in")
        af_feedrate = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Cutting Speed", af_speed)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate In", af_feedrate_in)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate", af_feedrate)

    async def set_wheels(self):
        """
        Load wheelpacks and set wheel segments
        """
        # Load wheelpack 1
        whp_name = self.configuration_wb.lookup("wheelpacks_1_3", "diameter", self.diam, "wheelpack_1")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 1)
        # Load wheelpack 2
        whp_name = self.configuration_wb.lookup("wheelpacks_1_3", "diameter", self.diam, "wheelpack_2")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 2)
        # Load wheelpack 4
        whp_name = self.configuration_wb.lookup("wheelpack_4", "diameter", self.diam, "wheelpack_4")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 4)
        # Load wheelpack 5
        whp_name = self.configuration_wb.lookup("wheelpack_5", "diameter", self.diam, "wheelpack_5")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 5)
        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpack_6", "diameter", self.diam, "wheelpack_6")
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, 6)

        # Set wheel segments for wheelpack 1
        # S_G1
        op_wh_seg = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)
        # RN
        op_wh_seg = self.configuration_wb.lookup("RN", "diameter", self.diam, "RN_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 2
        # TN1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Wheel", op_wh_seg)
        # SS
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Wheel", op_wh_seg)
        # P1
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
        # P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
        # S_P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)
        # No
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Wheel", op_wh_seg)
        # AF
        op_wh_seg = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 4
        # F1
        op_wh_seg = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 5
        # ERF
        op_wh_seg = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 6
        # G1
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
        # G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_wheel")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Wheel", op_wh_seg)

    async def set_isoeasy(self):
        """
        Load specified isoeasy program
        """
        isoeasy_raw_path = self.configuration_wb.lookup("isoeasy", "diameter", self.diam, "isoeasy_raw_path")
        await self.vgpc.load_isoeasy(isoeasy_raw_path)