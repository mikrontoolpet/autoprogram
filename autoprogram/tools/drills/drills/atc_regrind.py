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
    family_address = "drills/drills/atc_regrind"
    machine = "R628XW"

    def __init__(self, vgp_client, name, diameter, flute_length):
        super().__init__(vgp_client, name) # update class name here too!
        self.diam = float(diameter)
        self.fl_len = float(flute_length)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6.4)
        self.check_boundary(self.fl_len, 6*self.diam, 17.999*self.diam)

    def set_parameters(self):

        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")
        lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        tot_len = self.configuration_wb.lookup("blank", "diameter", self.diam, "tot_len")

        self.set("ns=2;s=tool/Blank/Profile/D", self.diam)
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
        # Profile
        point_ang = 141
        point_len = (self.diam/2)/math.tan(math.radians(point_ang/2))
        ta0 = -0.029
        sp1 = self.fl_len - 1.7*self.diam

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", point_ang)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", ta0)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", sp1)

        # Flute 1
        front_dl_start = 0.0374*self.diam + 0.1126
        fl_1_len = self.fl_len - 0.25*self.diam

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", fl_1_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", lead)

        # Flute 1 (G1)
        # Core diameter, rake angle and circular land width have a transition in values along the flute length
        g1_trans_len = 5*self.diam
        g1_len = fl_1_len
        g1_trans_perc = (g1_trans_len - point_len)/(g1_len - point_len)*100
        g1_trans_perc = round(g1_trans_perc, 3)
        g1_core_diam_perc_1 = 32
        g1_core_diam_perc_2 = 27
        g1_rake_ang_1 = 16
        g1_rake_ang_2 = 19
        g1_circ_land_width_1 = round(0.806*self.diam, 3)
        g1_circ_land_width_2 = round(0.756*self.diam, 3)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", "(s1;0%;" + str(g1_core_diam_perc_1) + "%);(s1;" + str(g1_trans_perc) + "%;" + str(g1_core_diam_perc_2) + "%);(s1;100%;" + str(g1_core_diam_perc_2) + "%)")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Rake Angle", "(s1;0%;" + str(g1_rake_ang_1) + "°);(s1;" + str(g1_trans_perc) + "%;" + str(g1_rake_ang_2) + "°);(s1;100%;" + str(g1_rake_ang_2) + "°)")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", "(s1;0%;" + str(g1_circ_land_width_1) + " mm);(s1;" + str(g1_trans_perc) + ";" + str(g1_circ_land_width_2) + " mm);(s1;100%;" + str(g1_circ_land_width_2) + " mm)")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Exit Radius", 0.25*self.diam)

        # Feeds and speeds
        g1_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_speed")
        g1_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (N_PP)
        n_pp_wheel_disp = 1 if self.diam < 1.5 else 2
        n_pp_dl_end = -round(3*self.diam, 2)
        n_pp_inf_down_y = round(0.5*self.diam, 2)
        n_pp_corr_y = round(-0.5*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel Displacement", n_pp_wheel_disp)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", n_pp_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", n_pp_inf_down_y)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Correction/Y", n_pp_corr_y)

        # Feeds and speeds
        # Always the same

        # Flute 1001 (G2)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", 5.47*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", lead)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", 1.0495*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Exit Radius", 0.1*self.diam)

        # Feeds and speeds
        g2_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_speed")
        g2_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Cutting Speed", g2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Feedrate", g2_feedrate)

        # Step 0
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance", 0.085*self.diam)
        
        # Gash (TN1)
        # Web thickness
        if self.diam <= 2:
            tn1_web_thick = 0.113*self.diam + 0.006
        elif self.diam < 4:
            tn1_web_thick = 0.107*self.diam + 0.018
        else:
            tn1_web_thick = 0.1235*self.diam - 0.028

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", tn1_web_thick)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)

        # Feeds and speeds
        tn1_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_speed")
        tn1_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate_in")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Cutting Speed", tn1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Feedrate In", tn1_feedrate_in)

        # # S-Gash (SS)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Web Thickness", -0.009*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", -0.065*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.175*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.0866*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.163*self.diam)

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
        pnt_frst_rlf = 16 if self.diam <= 4 else 13

        # Point Relief 1 (P1)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Relief Angle", pnt_frst_rlf)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL End", 0.04*self.diam + 0.06)

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
        # Point Relief 102
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 101/Relief Angle", pnt_frst_rlf)
        # Point Relief 102 (S_P2)
        # Feeds and speeds
        s_p2_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_speed")
        s_p2_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate_in")
        s_p2_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Cutting Speed", s_p2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate In", s_p2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate", s_p2_feedrate)

        # Set 2
        # OD Profile 2D
        self.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter_Drill", self.diam)

        # Gash 1 (No)
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/D", self.diam)

        # Relief 1 (AF)
        af_dl = 0.0467*self.diam + 0.1033
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/dL Start", af_dl)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/dL End", af_dl)
        # Feeds and speeds
        af_speed = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_speed")
        af_feedrate_in = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_feedrate_in")
        af_feedrate = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_feedrate")
        
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Cutting Speed", af_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate In", af_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate", af_feedrate)

    def set_wheels(self):
        """
        Load wheelpacks and set wheel segments
        """
        # Skip wheelpack 1
        # Load wheelpack 2
        whp_name = self.configuration_wb.lookup("wheelpacks_1_3", "diameter", self.diam, "wheelpack_2")
        self.set_wheel(whp_name, 2)
        # Skip wheelpack 3
        # Skip wheelpack 4
        # Load wheelpack 5
        whp_name = self.configuration_wb.lookup("wheelpack_5", "diameter", self.diam, "wheelpack_5")
        self.set_wheel(whp_name, 5)
        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpack_6", "diameter", self.diam, "wheelpack_6")
        self.set_wheel(whp_name, 6, "regrind")

    def set_wheel_segments(self):

        # Set wheel segments for wheelpack 2
        # TN1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Wheel", op_wh_seg)
        # SS
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Wheel", op_wh_seg)
        # P1
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
        # P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
        # S_P2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)
        # No
        op_wh_seg = self.configuration_wb.lookup("N_PP", "diameter", self.diam, "N_PP_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Wheel", op_wh_seg)
        # AF
        op_wh_seg = self.configuration_wb.lookup("AF", "diameter", self.diam, "AF_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 5
        # N_PP
        op_wh_seg = self.configuration_wb.lookup("N_PP", "diameter", self.diam, "N_PP_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 6
        # G1
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
        # G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_wheel")
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
        rl = 0.75*self.diam

        if (self.fl_len/self.diam - 3) <= 6:
            sm = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "sm_6xd")
        else:
            sm = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "sm_10xd")

        vf = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "vf")

        rl_text = "RL: " + str(rl) + " mm"
        sm_text = "SM: " + str(sm) + " mm"
        vf_text = "VF: " + str(vf) + " mm"

        coolant_text = "Attention to the coolant pipes position!!!"

        self.ds_text_args.append(rl_text)
        self.ds_text_args.append(sm_text)
        self.ds_text_args.append(vf_text)
        self.ds_text_args.append(coolant_text)

        # Images
        steadyrest_img_name = "steadyrest_setup"

        self.ds_img_names.append(steadyrest_img_name)