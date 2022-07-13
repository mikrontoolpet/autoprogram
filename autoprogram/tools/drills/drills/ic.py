from autoprogram.tools.basetool import BaseTool
import math

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
    machine = "R628XW"

    def __init__(self, vgp_client, name, diameter, flute_length):
        super().__init__(vgp_client, name) # update class name here too!
        self.diam = float(diameter)
        self.fl_len = float(flute_length)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6)
        self.check_boundary(self.fl_len, 7*self.diam, 17.999*self.diam)

    def set_parameters(self):
        # Set parameters
        self.lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")

        # Blank
        # Profile
        conic_len = 4.25*self.diam
        conic_len_p4 = conic_len + end_stk_rmv
        back_taper = 200
        neck_diam = self.diam - conic_len*(1/back_taper)
        tot_len = self.configuration_wb.lookup("blank", "diameter", self.diam, "tot_len_6_14xd") + end_stk_rmv

        self.set("ns=2;s=tool/Blank/Profile/Diameter", self.diam)
        self.set("ns=2;s=tool/Blank/Profile/Diameter neck", neck_diam)
        self.set("ns=2;s=tool/Blank/Profile/Length total", tot_len)

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
        fl_stk_rmv = min([0.08, 0.025*self.diam])
        d700 = self.common_wb.lookup("D700", "diameter", self.diam, "D700")

        self.set("ns=2;s=tool/Tool/Reference Length (RL)", 1.5*self.diam)
        self.set("ns=2;s=tool/Tool/End Stock Removal (dL)", end_stk_rmv)
        self.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", d700)
        self.set("ns=2;s=tool/Tool/Set 2/Cutting Security Distance", d700)
        self.set("ns=2;s=tool/Tool/Set 3/Cutting Security Distance", d700)

        # Set 1
        # Profile
        point_ang = 141
        point_len = (self.diam/2)/math.tan(math.radians(point_ang/2))
        sp1_len = 4.35*self.diam - point_len + 0.13*self.diam

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", point_ang)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", sp1_len)

        # Flute 1
        front_dl_start = 0.2
        front_fl_len = 3.225*self.diam
        back_fl_len = self.fl_len - front_fl_len
        fl_len_end_diff = 0.275*self.diam

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", front_fl_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G1)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL End", 1.2*self.diam)

        # Feeds and speeds
        g1_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_speed")
        g1_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (G2)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", 0.0185*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", 0.8*self.diam)

        # Feeds and speeds
        g2_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_speed")
        g2_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Cutting Speed", g2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate", g2_feedrate)

        # Flute 201 (S_G1)
        s_g1_att_ang = self.configuration_wb.trend("function_data", "diameter", self.diam, "S_G1_attack_angle")
        rs = -0.025*self.diam

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", rs)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Attack Angle", s_g1_att_ang)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL End", 1.6*self.diam)

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
        # OD Clearance 1 (F1)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Margin Width", 0.0757*self.diam)
        # Feeds and speeds
        f1_speed = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_speed")
        f1_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Cutting Speed", f1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 1/Feedrate", f1_feedrate)

        # OD Clearance 101 (F2)
        f2_marg_width = self.configuration_wb.trend("function_data", "diameter", self.diam, "F2_margin_width")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Margin Width", f2_marg_width)

        # Feeds and speeds
        f2_speed = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_speed")
        f2_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F12_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Cutting Speed", f2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/OD Clearance 101/Feedrate", f2_feedrate)

        # Set 2
        # Profile
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Profile/sP1", self.diam)

        # Flute 1
        back_fl_len = self.fl_len - front_fl_len
        back_infeed_down_y = 0.375*self.diam + 0.3 # flute depth + security distance

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Custom Profile Flute/dZ", -front_fl_len)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Custom Profile Flute/D", self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Custom Profile Flute/L", back_fl_len)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G3)
        g3_dl_start = self.configuration_wb.trend("function_data", "diameter", self.diam, "G3_dl_start")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", g3_dl_start)  
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL End", -0.25*self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Infeed Down Y", back_infeed_down_y)

        # Feeds and speeds
        g3_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G3_speed")
        g3_feedrate_in = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G3_feedrate_in")
        g3_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G3_feedrate")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g3_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate In", g3_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g3_feedrate)

        # Flute 101 (S_G3)
        s_g3_att_ang = self.configuration_wb.trend("function_data", "diameter", self.diam, "S_G3_attack_angle")
        s_g3_dl_start = g3_dl_start

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", rs)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Attack Angle", s_g3_att_ang)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/dL Start", s_g3_dl_start)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/dL End", -0.17*self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", back_infeed_down_y)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Exit Radius", 0.333*self.diam)

        # Feeds and speeds
        s_g3_speed = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G3_speed")
        s_g3_feedrate_in = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G3_feedrate_in")
        s_g3_feedrate = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G3_feedrate")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Cutting Speed", s_g3_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Feedrate In", s_g3_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Feedrate", s_g3_feedrate)

        # Flute 201 (RN1)
        rn1_dl_start = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN1_dl_start")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", 0.028*self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/dL Start", rn1_dl_start)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/dL End", -0.8*self.diam)

        # Feeds and speeds
        rn12_speed = self.configuration_wb.lookup("rn", "diameter", self.diam, "RN12_speed")
        rn12_feedrate_in = self.configuration_wb.lookup("rn", "diameter", self.diam, "RN12_feedrate_in")
        rn12_feedrate = self.configuration_wb.lookup("rn", "diameter", self.diam, "RN12_feedrate")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Cutting Speed", rn12_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Feedrate In", rn12_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Feedrate", rn12_feedrate)

        # Flute 301 (RN2)
        rn_2_rake_shift = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN2_rake_shift")
        rn2_dl_start = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN2_dl_start")
        rn2_infeed_z = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN2_infeed_z")
        rn2_infeed_y = self.configuration_wb.trend("function_data", "diameter", self.diam, "RN2_infeed_y")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Rake Shift", rn_2_rake_shift)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/dL Start", rn2_dl_start)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/dL End", -0.8*self.diam)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Infeed Motion (Start)/Z", rn2_infeed_z)

        # Feeds and speeds
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Cutting Speed", rn12_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Feedrate In", rn12_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Feedrate", rn12_feedrate)

        # Set 3
        # OD Profile 2D
        self.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Diameter", self.diam)
        self.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Distance", 0.3*self.diam)

        # Gash 1 (TN2)
        tn2_index = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN2_index")
        tn2_web_thck = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN2_web_thickness")

        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Index", tn2_index)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/D", 1.17*self.diam)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/dD", 0.943*self.diam)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/dZ", -0.168*self.diam)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Web Thickness", tn2_web_thck)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Profile 2D/sR", 0.263*self.diam)

        # Feeds and speeds
        tn2_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_speed")
        tn2_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate_in")
        tn2_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Cutting Speed", tn2_speed)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Feedrate In", tn2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Feed along sweep+exit", tn2_feedrate)

        # Relief 1 (SM)
        self.set("ns=2;s=tool/Tool/Set 3/Reliefs/Relief Section 1/Relief 1/Cam 1/Exit distance", 0.2*self.diam)

        # Feeds and speeds
        sm_speed = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_speed")
        sm_feedrate_in = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_feedrate_in")
        sm_feedrate = self.configuration_wb.lookup("chamfer", "diameter", self.diam, "SM_feedrate")

        self.set("ns=2;s=tool/Tool/Set 3/Reliefs/Relief Section 1/Relief 1/Cutting Speed", sm_speed)
        self.set("ns=2;s=tool/Tool/Set 3/Reliefs/Relief Section 1/Relief 1/Feedrate In", sm_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 3/Reliefs/Relief Section 1/Relief 1/Feedrate", sm_feedrate)

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

        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpack_6", "diameter", self.diam, "wheelpack_6")

        self.set_wheel(whp_name, 6)

    def set_wheel_segments(self):
        # Set wheel segments for wheelpack 1
        # S_G1
        op_wh_seg = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G1_wheel")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)

        # S_G3
        op_wh_seg = self.configuration_wb.lookup("roughing_flutes", "diameter", self.diam, "S_G3_wheel")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)

        # RN1
        op_wh_seg = self.configuration_wb.lookup("rn", "diameter", self.diam, "RN12_wheel")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)

        # RN2
        op_wh_seg = self.configuration_wb.lookup("rn", "diameter", self.diam, "RN12_wheel")

        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 301/Wheel", op_wh_seg)

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

        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Wheel", op_wh_seg)

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

        self.set("ns=2;s=tool/Tool/Set 3/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 6
        # G1
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)

        # G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_wheel")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)

        # G3
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G3_wheel")
        
        self.set("ns=2;s=tool/Tool/Set 2/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)

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
        self.ds_text_args.append(coolant_text)

        # Images
        support_len_img_name = str(support_len) + "mm"

        self.ds_img_names.append(support_len_img_name)