from autoprogram.tools.basetool import BaseTool
import math


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
    family_address = "drills/drills/ptc"
    machine = "R628XW"

    def __init__(self, vgp_client, name, diameter, flute_length):
        super().__init__(vgp_client, name) # update class name here too!
        self.diam = float(diameter)
        self.fl_len = float(flute_length)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6.4)
        self.check_boundary(self.fl_len, 6*self.diam, 17.999*self.diam)

    async def set_parameters(self):

        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")
        lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        tot_len = self.configuration_wb.lookup("blank", "diameter", self.diam, "tot_len")
        self.set("ns=2;s=tool/Blank/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Blank/Profile/L", tot_len)

        # Coolant holes
        # Group 1
        hole_cent_rad_1 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_1")
        hole_diam_1 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_1")

        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Helicoidal Holes/Helicoidal Holes/Lead", lead)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Distance from center", hole_cent_rad_1)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Holes Diameter", hole_diam_1)

        # Group 2
        hole_cent_rad_2 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_2")
        hole_diam_2 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_2")

        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Helicoidal Holes/Helicoidal Holes/Lead", lead)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Distance from center", hole_cent_rad_2)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Holes Diameter", hole_diam_2)

        # Group 3
        hole_cent_rad_3 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_3")
        hole_diam_3 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_3")

        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Helicoidal Holes/Helicoidal Holes/Lead", lead)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Distance from center", hole_cent_rad_3)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Holes Diameter", hole_diam_3)

        # Set parameters
        # Set 1
        # Common Data
        d700 = self.common_wb.lookup("D700", "diameter", self.diam, "D700")

        self.set("ns=2;s=tool/Tool/Reference Length (RL)", 0.75*self.diam)
        self.set("ns=2;s=tool/Tool/End Stock Removal (dL)", end_stk_rmv)
        self.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", d700)
        self.set("ns=2;s=tool/Tool/Set 2/Cutting Security Distance", d700)

       # Set 1
        # Common Data
        point_ang = 140
        point_len = (self.diam/2)/math.tan(math.radians(point_ang/2))
        ta0 = -0.143
        sp1_coeff = self.configuration_wb.lookup("function_data", "diameter", self.diam, "COMMON_DATA_sp1_coefficent")
        sp1 = round(sp1_coeff*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", sp1)

        # Flute 1
        front_dl_start = round(0.0374*self.diam + 0.1126, 2)
        prog_fl_len = round(self.fl_len - 0.25*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", prog_fl_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", lead)

        # Flute 1 (G1)
        # Core diameter, rake angle and circular land width have a transition in values along the flute length
        g1_core_diam_perc_1 = 34
        g1_core_diam_perc_2 = 31
        g1_circ_land_width = round(0.791*self.diam, 2)
        g1_exit_rad = round(0.25*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", g1_circ_land_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Exit Radius", g1_exit_rad)

        # Feeds and speeds
        g1_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_speed")
        g1_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (S_G1)
        """
        Roughing flute has 2 stock removals:
        - one for the rake
        - one for the core
        """
        s_g1_rake_rad_stk_rmv = 0.008*self.diam + 0.012 # rake radial stock removal
        s_g1_core_rad_stk_rmv = 0.007*self.diam + 0.018 # core radial stock removal
        s_g1_core_rad_stk_rmv_perc = s_g1_core_rad_stk_rmv/self.diam*100 # radial stock removal percentage
        s_g1_core_stk_rmv_perc = 2*s_g1_core_rad_stk_rmv_perc # total stock removal percentage
        s_g1_core_diam_perc_1 = round(g1_core_diam_perc_1 + s_g1_core_stk_rmv_perc, 1)
        s_g1_core_diam_perc_2 = round(g1_core_diam_perc_2 + s_g1_core_stk_rmv_perc, 1)
        s_g1_circ_land_width = round(0.808*self.diam, 2)
        s_g1_dl_end = round(0.075*self.diam, 2)
        s_g1_exit_rad = round(0.5*self.diam, 2)
        s_g1_inf_down_y = round(0.04*self.diam + 0.06, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", -s_g1_rake_rad_stk_rmv)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", str(s_g1_core_diam_perc_1) + "%;" + str(s_g1_core_diam_perc_2) + "%")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Circular Land Width", s_g1_circ_land_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", s_g1_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Exit Radius", s_g1_exit_rad)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", s_g1_inf_down_y)

        # Feeds and speeds
        s_g1_speed = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_speed")
        s_g1_feedrate_in = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_feedrate_in")
        s_g1_feedrate = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Cutting Speed", s_g1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate In", s_g1_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate", s_g1_feedrate)

        # Flute 301 (ERF)
        erf_dl_start = round(-2.5*self.diam, 2)
        erf_dl_end = round(0.5*self.diam, 2)
        erf_inf_down_y = round(0.5*self.diam, 2)
        erf_corr_y = round(-0.5*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/dL Start", erf_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/dL End", erf_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Infeed Down Y", erf_inf_down_y)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Correction/Y", erf_corr_y)

        # Feeds and speeds
        erf_speed = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_speed")
        erf_feedrate_in = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_feedrate_in")
        erf_feedrate = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Cutting Speed", erf_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Feedrate In", erf_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Feedrate", erf_feedrate)

        # Flute 1001 (G2)
        g2_circ_land_width = round(1.087*self.diam, 2)
        g2_exit_rad = round(0.25*self.diam, 2)
        g2_dl_end = round(-0.25*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", prog_fl_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", lead)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", g2_circ_land_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL End", g2_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Exit Radius", g2_exit_rad)

        # Feeds and speeds
        g2_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_speed")
        g2_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Cutting Speed", g2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Feedrate", g2_feedrate)

        # Step 0
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance", 0.0886*self.diam)

        # Gash (TN1)
        # Web thickness
        tn1_index = self.configuration_wb.lookup("function_data", "diameter", self.diam, "TN1_index")
        tn1_web_thick = 0.1264*self.diam - 0.0024

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", tn1_index)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", tn1_web_thick)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)

        # Feeds and speeds
        tn1_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_speed")
        tn1_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate_in")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Cutting Speed", tn1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Feedrate In", tn1_feedrate_in)

        # # S-Gash (SS)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", -0.0538*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.175*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.0866*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.25*self.diam)

        # Feeds and speeds
        ss_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_speed")
        ss_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate_in")
        ss_feedrate_rotation = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate_rotation")
        ss_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Cutting Speed", ss_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feedrate In", ss_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feedrate", ss_feedrate_rotation)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feed along sweep", ss_feedrate)

        # Point Relief
        # Relief 1

        # Point Relief 1 (P1)
        # Feeds and speeds
        p1_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_speed")
        p1_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_feedrate_in")
        p1_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Cutting Speed", p1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Feedrate In", p1_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Feedrate", p1_feedrate)

        # Point Relief 2 (P2)
        # Feeds and speeds
        p2_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_speed")
        p2_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_feedrate_in")
        p2_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Cutting Speed", p2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Feedrate In", p2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Feedrate", p2_feedrate)

        # Relief 101
        # Point Relief 102 (S_P2)
        # Feeds and speeds
        s_p2_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_speed")
        s_p2_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate_in")
        s_p2_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Cutting Speed", s_p2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate In", s_p2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate", s_p2_feedrate)

        # Step 0 Diameter
        # Step 0 OD Clearance
        # OD Clearance 1 (F1)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", 0.075*self.diam)

        # Feeds and speeds
        f12r_speed = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12R_speed")
        f1_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Cutting Speed", f12r_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Feedrate", f1_feedrate)

        # OD Clearance 101 (F2)
        f2_marg_width = self.configuration_wb.lookup("function_data", "diameter", self.diam, "F2_margin_width")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", f2_marg_width)

        # Feeds and speeds
        f2_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Cutting Speed", f12r_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Feedrate", f2_feedrate)

        # OD Clearance 201 (FR)
        fr_marg_width = round(0.62*self.diam, 2)
        fr_bk_clear_perc = self.configuration_wb.lookup("function_data", "diameter", self.diam, "FR_back_clearance")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Margin Width", fr_marg_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Back Clearance", fr_bk_clear_perc)

        # Feeds and speeds
        fr_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "FR_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Cutting Speed", f12r_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Feedrate", fr_feedrate)

        # Set 2
        # OD Profile 2D
        self.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter_Drill", self.diam)

        # Gash 1 (TN2)
        tn2_d = 1.17*self.diam
        tn2_dd = 0.925*self.diam
        tn2_dz = -0.165*self.diam
        tn2_web_thck = -0.056*self.diam
        tn2_sr = 0.3*self.diam

        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/D", tn2_d)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/dD", tn2_dd)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/dZ", tn2_dz)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Web Thickness", tn2_web_thck)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Profile 2D/sR", tn2_sr)

        # Feeds and speeds
        tn2_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_speed")
        tn2_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate_in")
        tn2_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate")
        
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Cutting Speed", tn2_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Feedrate In", tn2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Feed along sweep+exit", tn2_feedrate)

        # Gash 1001 (No)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1001/Virtual Profile/D", self.diam)

        # Relief 1 (AF)
        af_dl = round(0.0467*self.diam + 0.1033, 2)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/dL Start", af_dl)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/dL End", af_dl)

        # Feeds and speeds
        af_speed = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_speed")
        af_feedrate_in = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_feedrate_in")
        af_feedrate = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_feedrate")

        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Cutting Speed", af_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate In", af_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate", af_feedrate)

        # Relief 2 (SM)
        sm_exit_dist = round(0.14*self.diam + 0.16, 2)
        sm_depth = 0.005*self.diam - 0.002

        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Exit distance", sm_exit_dist)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cam 1/Depth", sm_depth)

        # Feeds and speeds
        sm_speed = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_speed")
        sm_feedrate_in = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_feedrate_in")
        sm_feedrate = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_feedrate")

        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Cutting Speed", sm_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Feedrate In", sm_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Feedrate", sm_feedrate)

    def set_wheels(self):
        """
        Load wheelpacks
        """
        # Load wheelpack 1
        whp_name = self.configuration_wb.lookup("wheelpacks_1_3", "diameter", self.diam, "wheelpack_1")
        self.set_wheel(whp_name, 1)
        # Load wheelpack 2
        whp_name = self.configuration_wb.lookup("wheelpacks_1_3", "diameter", self.diam, "wheelpack_2")
        self.set_wheel(whp_name, 2)
        # Skip wheelpack 3
        # Load wheelpack 4
        whp_name = self.configuration_wb.lookup("wheelpack_4", "diameter", self.diam, "wheelpack_4")
        self.set_wheel(whp_name, 4)
        # Load wheelpack 5
        whp_name = self.configuration_wb.lookup("wheelpack_5", "diameter", self.diam, "wheelpack_5")
        self.set_wheel(whp_name, 5)
        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpack_6", "diameter", self.diam, "wheelpack_6")
        self.set_wheel(whp_name, 6)

    def set_wheel_segments(self):
        # Set wheel segments for wheelpack 1
        # S_G1
        op_wh_seg = self.configuration_wb.lookup("roughing_flute", "diameter", self.diam, "S_G1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 2
        # TN1 - TN2
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Wheel", op_wh_seg)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Wheel", op_wh_seg)
        # SS
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Wheel", op_wh_seg)
        # P1 - P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
        # S_P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)
        # SM
        op_wh_seg = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 2/Relief 1/Wheel", op_wh_seg)
        # No
        op_wh_seg = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1001/Wheel", op_wh_seg)
        # AF
        op_wh_seg = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 4
        # F1 - F2 - FR
        op_wh_seg = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12R_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Wheel", op_wh_seg)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Wheel", op_wh_seg)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 201/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 5
        # ERF
        op_wh_seg = self.configuration_wb.lookup("ERF", "diameter", self.diam, "ERF_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 6
        # G1 - G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Wheel", op_wh_seg)

    def set_isoeasy(self):
        """
        Set isoeasy
        """
        self.isoeasy_name = self.configuration_wb.lookup("isoeasy", "diameter", self.diam, "isoeasy_name")

    def set_datasheet(self):
        """
        Write additional information on datasheet
        """
        # Text
        if (self.fl_len/self.diam - 3) <= 6:
            support_len = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "support_len_6xd")
        else:
            support_len = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "support_len_10xd")
        support_len = round(support_len)
        support_len_text = "Support length: " + str(support_len) + " mm"
        coolant_text = "Attention to the coolant pipes position!!!"

        self.ds_text_args.append(support_len_text)

        # Images
        support_len_img_name = str(support_len) + "mm"
        coolant_img_name = "coolant"

        self.ds_img_names.append(support_len_img_name)
        self.ds_img_names.append(coolant_img_name)