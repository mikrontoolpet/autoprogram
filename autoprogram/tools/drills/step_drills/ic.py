from autoprogram.tools.basetool import BaseTool
import math

class Tool(BaseTool):
    """
    CrazyDrill CoolPilot (PD.090.IC) drill class
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/step_drills/ic"
    machine = "R628XW"

    def __init__(self, vgp_client, name, diameter, step_length, step_diameter, flute_length):
        super().__init__(vgp_client, name) # update class name here too!
        self.diam = float(diameter)
        self.step_len = float(step_length)
        self.step_diam = float(step_diameter)
        self.fl_len = float(flute_length)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6)

    def set_parameters(self):
        # Set parameters
        point_ang = 143
        step_ang = 45
        self.lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")
        point_len = (self.diam/2)/math.tan(math.radians(point_ang/2))

        # Blank
        # Profile
        blank_step_len = self.step_len + point_len
        tot_len = self.configuration_wb.lookup("blank", "diameter", self.diam, "tot_len") + end_stk_rmv

        self.set("ns=2;s=tool/Blank/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Blank/Profile/D1", self.step_diam)
        self.set("ns=2;s=tool/Blank/Profile/sP1", blank_step_len)
        self.set("ns=2;s=tool/Blank/Profile/L", tot_len)

        # Coolant holes
        # Group 1
        hole_cent_rad_1 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_1")
        hole_diam_1 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_1")

        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Helicoidal Holes/Helicoidal Holes/Lead", self.lead)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Distance from center", hole_cent_rad_1)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 1/Holes Diameter", hole_diam_1)

        # Group 2
        hole_cent_rad_2 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_2")
        hole_diam_2 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_2")

        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Helicoidal Holes/Helicoidal Holes/Lead", self.lead)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Distance from center", hole_cent_rad_2)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 2/Holes Diameter", hole_diam_2)

        # Group 3
        hole_cent_rad_3 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_cent_rad_3")
        hole_diam_3 = self.configuration_wb.lookup("blank", "diameter", self.diam, "hole_diam_3")

        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Helicoidal Holes/Helicoidal Holes/Lead", self.lead)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Distance from center", hole_cent_rad_3)
        self.set("ns=2;s=tool/Blank/Coolant Holes/Group 3/Holes Diameter", hole_diam_3)

        # Common Data
        d700 = self.common_wb.lookup("D700", "diameter", self.diam, "D700")

        self.set("ns=2;s=tool/Tool/Reference Length (RL)", self.step_len + 3*self.diam)
        self.set("ns=2;s=tool/Tool/End Stock Removal (dL)", end_stk_rmv)
        self.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", d700)
        self.set("ns=2;s=tool/Tool/Set 2/Cutting Security Distance", d700)

        # Set 1
        # Profile
        step_corr_len = 0.1*self.diam
        back_len = self.step_len + (self.step_diam - self.diam)/2/math.tan(math.radians(step_ang)) + step_corr_len

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D1", self.step_diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", self.step_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP2", back_len)

        # Flute 1
        atk_ang_front_len = self.step_len - 1.15*self.diam
        atk_ang_back_len = self.step_len - 0.15*self.diam
        atk_ang_front_perc = atk_ang_front_len/(self.fl_len - point_len)*100
        atk_ang_back_perc = atk_ang_back_len/(self.fl_len - point_len)*100
        front_dl_start = 0.2

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", self.fl_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G1)
        g1_atk_ang_str = "(s1;0%;0.5°);(s1;" + str(atk_ang_front_perc) + "%;0.5°);(s1;" + str(atk_ang_back_perc) + "%;10°);(s1;100%;10°)"

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Attack Angle", g1_atk_ang_str)

        # Feeds and speeds
        g1_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_speed")
        g1_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (G2)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", 0.018*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", -0.2*self.diam)

        # Feeds and speeds
        g2_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_speed")
        g2_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Cutting Speed", g2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate", g2_feedrate)

        # Flute 201 (S_G1)
        s_g1_atk_ang_front = self.configuration_wb.lookup("function_data", "diameter", self.diam, "S_G1_attack_angle_front")
        s_g1_atk_ang_back = self.configuration_wb.lookup("function_data", "diameter", self.diam, "S_G1_attack_angle_back")
        s_g1_atk_ang_str = "(s1;0%;" + str(s_g1_atk_ang_front) + "°);(s1;" + str(atk_ang_front_perc) + "%;" + str(s_g1_atk_ang_front) + "°);(s1;" + str(atk_ang_back_perc) + "%;" + str(s_g1_atk_ang_back) + "°);(s1;100%;" + str(s_g1_atk_ang_back) + "°)"

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", -0.025*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Attack Angle", s_g1_atk_ang_str)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL End", -0.0638*self.step_diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Exit Radius", 0.5*self.diam)

        # Feeds and speeds
        s_g1_speed = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G1_speed")
        s_g1_feedrate = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Cutting Speed", s_g1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Feedrate", s_g1_feedrate)

        # Step 0
        sc = 0.008*self.diam
        s1_rake = 2
        tn3_rake = -10
        tn3_width = self.configuration_wb.lookup("tn_width", "diameter", self.diam, "tn_width")
        s1_offset = tn3_width*(math.tan(math.radians(s1_rake)) + math.tan(math.radians(-tn3_rake)))
        s1_web_thck = sc + s1_offset

        # Gash 1 (S1)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Web Thickness", s1_web_thck)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Depth Past Center Yp", -0.02429*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Straight Gash/Profile 2D/sR", 0.0649*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Straight Gash/Profile 2D/sL", 0.55*self.diam)

        # Feeds and speeds
        s1_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "S1_speed")
        s1_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "S1_feedrate_in")
        s1_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "S1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Straight Gash/Cutting Speed", s1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Straight Gash/Feedrate In", s1_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Straight Gash/Feed along sweep+exit", s1_feedrate)

        # Gash 101 (TN3)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Web Thickness", sc)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Depth Past Center Yp", -0.03*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Straight Gash/Profile 2D/sR", 0.0649*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Straight Gash/Profile 2D/sL", 0.0786*self.diam)

        # Feeds and speeds
        tn3_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN3_speed")
        tn3_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN3_feedrate_in")
        tn3_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN3_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Straight Gash/Cutting Speed", tn3_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Straight Gash/Feedrate In", tn3_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Straight Gash/Feed along sweep+exit", tn3_feedrate)

        # Gash 201 (TN1)
        tn1_web_thck = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN1_web_thickness")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Web Thickness", tn1_web_thck)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Depth Past Center Yp", -0.2*self.diam)

        # Feeds and speeds
        tn1_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_speed")
        tn1_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate_in")
        tn1_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Straight Gash/Cutting Speed", tn1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Straight Gash/Feedrate In", tn1_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Straight Gash/Feed along sweep+exit", tn1_feedrate)

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
        f12_dl_end = tn1_web_thck = self.configuration_wb.trend("function_data", "diameter", self.diam, "F12_dl_end")
        # OD Clearance 1 (F1)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", 0.072*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/dL End", f12_dl_end)

        # Feeds and speeds
        f1_speed = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_speed")
        f1_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Cutting Speed", f1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Feedrate", f1_feedrate)

        # OD Clearance 101 (F2)
        f2_marg_width = self.configuration_wb.trend("function_data", "diameter", self.diam, "F2_margin_width")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", f2_marg_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/dL End", f12_dl_end)

        # Feeds and speeds
        f2_speed = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_speed")
        f2_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Cutting Speed", f2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Feedrate", f2_feedrate)

        # Step 1
        # Step 1 Gash
        rp_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "RP_index")
        rp_web_thck = self.configuration_wb.trend("function_data", "diameter", self.diam, "RP_web_thickness")
        rp_yp = self.configuration_wb.trend("function_data", "diameter", self.diam, "RP_yp")
        rp_rot_c = self.configuration_wb.trend("function_data", "diameter", self.diam, "RP_rotation_c")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Index", rp_index)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Web Thickness", rp_web_thck)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Depth Past Center Yp", rp_yp)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Rotation C", rp_rot_c)

        # Step 1 Step Reliefs
        gr_radial_relief = self.configuration_wb.trend("function_data", "diameter", self.diam, "GR_radial_relief_angle")
        gr_axial_relief = 13 if self.diam < 1.5 else 10
        gr_rot_c = self.configuration_wb.trend("function_data", "diameter", self.diam, "GR_rotation_c")
        gr_depth = self.configuration_wb.trend("function_data", "diameter", self.diam, "GR_depth")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Radial Relief Angle", gr_radial_relief)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Axial Relief Angle", gr_axial_relief)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Rotation C", gr_rot_c)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Depth", gr_depth)

        # Set 2
        # OD Profile 2D
        self.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter", self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Distance", 0.2967*self.diam)

        # Gash 1 (TN2)
        tn2_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN2_index")
        tn2_web_thck = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN2_web_thickness")

        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Index", tn2_index)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/D", 1.17*self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/dD", 0.943*self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/dZ", -0.168*self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Web Thickness", tn2_web_thck)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Profile 2D/sR", 0.263*self.diam)

        # Feeds and speeds
        tn2_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_speed")
        tn2_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate_in")
        tn2_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Cutting Speed", tn2_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Feedrate In", tn2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Feed along sweep+exit", tn2_feedrate)

        # Relief 1 (SM)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Cam 1/Exit distance", 0.2*self.diam)

        # Feeds and speeds
        sm_speed = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_speed")
        sm_feedrate_in = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_feedrate_in")
        sm_feedrate = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_feedrate")

        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Cutting Speed", sm_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate In", sm_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate", sm_feedrate)

    def set_wheels(self):
        """
        Load wheelpacks and set wheel segments
        """
        # Load wheelpack 1
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_1")
        self.set_wheel(whp_name, 1)

        # Load wheelpack 2
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_2")
        self.set_wheel(whp_name, 2)

        # Load wheelpack 3
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_3")
        self.set_wheel(whp_name, 3)

        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpack_6", "diameter", self.diam, "wheelpack_6")
        self.set_wheel(whp_name, 6)

    def set_wheel_segments(self):
        # Set wheel segments for wheelpack 1
        # S_G1
        op_wh_seg = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)

        # F1
        op_wh_seg = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Wheel", op_wh_seg)

        # F2
        op_wh_seg = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 2
        # S1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "S1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 1/Straight Gash/Wheel", op_wh_seg)

        # TN1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 201/Straight Gash/Wheel", op_wh_seg)

        # TN2
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Wheel", op_wh_seg)

        # TN3
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN3_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash 101/Straight Gash/Wheel", op_wh_seg)

        # P1
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)

        # P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)

        # S_P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)

        # SM
        op_wh_seg = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 3
        # RP
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "RP_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Wheel", op_wh_seg)

        # GR
        op_wh_seg = self.configuration_wb.lookup("step_relief", "diameter", self.diam, "GR_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 6
        # G1
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)

        # G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)

    def set_isoeasy(self):
        """
        Set isoeasy
        """
        pass
        # self.isoeasy_name = self.configuration_wb.lookup("isoeasy", "diameter", self.diam, "isoeasy_name")

    def set_datasheet(self):
        """
        Write additional information on datasheet
        """
        pass