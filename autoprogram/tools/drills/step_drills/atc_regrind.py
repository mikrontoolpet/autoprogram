from autoprogram.tools.basetool import BaseTool
import math


class Tool(BaseTool):
    """
    Pilot Drill Titanium Grade 5 (ATC)
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/step_drills/atc_regrind"
    machine = "R628XW"

    def __init__(self, vgp_client, name, diameter, step_length, step_diameter, flute_length):
        super().__init__(vgp_client, name) # update class name here too!
        self.diam = float(diameter)
        self.step_len = float(step_length)
        self.step_diam = float(step_diameter)
        self.fl_len = float(flute_length)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6.35)

    async def set_parameters(self):
        # Set parameters
        point_ang = 144
        step_ang = 45
        self.lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")
        trig_point_len = (self.diam/2)/math.tan(math.radians(point_ang/2))

        # Blank
        # Profile
        blank_step_len = self.step_len + trig_point_len
        tot_len = self.fl_len + 2*self.diam

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
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D1", self.step_diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", self.step_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP2", self.step_len + 0.5*self.diam)

        # Flute 1
        front_dl_start = round(0.03*self.diam + 0.12, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", self.fl_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G1)
        g1_core_diam_perc = 32
        g1_rake_ang = 16
        g1_exit_rad = round(0.1666*self.diam, 2)
        g1_circ_lnd_width = round(0.795*self.diam, 2)
        g1_dl_end = round(-0.1666*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", g1_circ_lnd_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL End", g1_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Exit Radius", g1_exit_rad)

        # Feeds and speeds
        g1_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_speed")
        g1_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Cutting Speed", g1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (N_PP)
        n_pp_wheel_disp = 1 if self.diam < 1.5 else 2
        n_pp_dl_end = round(-self.fl_len + self.step_len + 1.5*self.diam, 2) # - self.fl_len + 4.5*self.diam in the original document 
        n_pp_inf_down_y = round(0.5*self.diam, 2)
        n_pp_corr_y = round(-0.5*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel Displacement", n_pp_wheel_disp)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", n_pp_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", n_pp_inf_down_y)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Correction/Y", n_pp_corr_y)

        # Feeds and speeds
        # Always the same

        # Flute 1001
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", self.fl_len)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", self.lead)

        # Flute 1 (G2)
        g2_circ_lnd_width = round(1.0495*self.diam, 2)
        g2_dl_end = round(-0.25*self.diam, 2)
        g2_exit_rad = round(0.1666*self.diam, 2)

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", g2_circ_lnd_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL Start", front_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL End", g2_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Exit Radius", g2_exit_rad)

        # Feeds and speeds
        g2_speed = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_speed")
        g2_feedrate = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Cutting Speed", g2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Feedrate", g2_feedrate)

        # Step 0
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance", 0.08*self.diam)

        # Gash (TN1)
        tn1_index = self.configuration_wb.lookup("function_data", "diameter", self.diam, "TN1_index")
        tn1_web_thck = self.configuration_wb.lookup("function_data", "diameter", self.diam, "TN1_web_thickness")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", tn1_index)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", tn1_web_thck)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)

        # Feeds and speeds
        tn1_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_speed")
        tn1_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate_in")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Cutting Speed", tn1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Feedrate In", tn1_feedrate_in)

        # S-Gash (SS)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Web Thickness", -0.009*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", -0.065*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.175*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.0866*self.diam)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.17*self.diam)

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
        pnt_frst_rlf = 15 if self.diam <= 4 else 12

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
        # Point Relief 101
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 101/Relief Angle", pnt_frst_rlf)

        # Point Relief 102 (S_P2)
        # Feeds and speeds
        s_p2_speed = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_speed")
        s_p2_feedrate_in = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate_in")
        s_p2_feedrate = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Cutting Speed", s_p2_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate In", s_p2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Feedrate", s_p2_feedrate)

        # Step 0 Diameter
        delta_dl = await self.get("ns=2;s=tool/Tool/Set 1/Delta dL (Output)")
        point_len = trig_point_len + delta_dl

        # Step 0 OD Clearance
        f1_sett_ang = self.configuration_wb.lookup("function_data", "diameter", self.diam, "F1_setting_angle")

        # OD Clearance 1 (F1)
        f1_marg_width = round(0.1*self.diam, 2)
        f1_dl_start = -(self.step_len - 0.25*self.diam)
        f1_dl_end = self.configuration_wb.lookup("function_data", "diameter", self.diam, "F1_dl_end")
        f1_c_rot_end = self.configuration_wb.lookup("function_data", "diameter", self.diam, "F1_c_rotation_at end")
        f1_c_rot_ax = 10 if self.diam >= 1.5 else 13

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Margin Width", f1_marg_width)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Setting Angle", f1_sett_ang)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/dL Start", f1_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/dL End", f1_dl_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/C Rotation at end", f1_c_rot_end)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Rotation C axial angle", f1_c_rot_ax)

        # Feeds and speeds
        f1_speed = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_speed")
        f1_feedrate = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Cutting Speed", f1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Feedrate", f1_feedrate)

        # Step 1
        # Step 1 Gash (RD)
        rd_index = self.configuration_wb.lookup("function_data", "diameter", self.diam, "RD_index")
        rd_d = self.configuration_wb.lookup("function_data", "diameter", self.diam, "RD_d")
        rd_dd = self.diam
        rd_dz = -(self.step_len + point_len)
        rd_web_thckn = self.configuration_wb.lookup("function_data", "diameter", self.diam, "RD_web_thickness")
        rd_yp = self.configuration_wb.lookup("function_data", "diameter", self.diam, "RD_yp")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Index", rd_index)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Virtual Profile/D", rd_d)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Virtual Profile/dD", rd_dd)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Virtual Profile/dZ", rd_dz)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Web Thickness", rd_web_thckn)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Depth Past Center Yp", rd_yp)

        # Feeds and speeds
        rd_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "RD_speed")
        rd_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "RD_feedrate_in")
        rd_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "RD_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Cutting Speed", rd_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Feedrate In", rd_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Feed along sweep+exit", rd_feedrate)

        # Step 1 Step Reliefs (GR)
        gr_rad_rel = 0.7 if self.diam < 3 else 1
        gr_ax_rel = 10 if self.diam >= 1.5 else 13
        gr_dl_start = self.configuration_wb.lookup("function_data", "diameter", self.diam, "GR_dl_start")
        gr_rot_c = 72 if self.diam < 3 else 80
        gr_depth = self.configuration_wb.lookup("function_data", "diameter", self.diam, "GR_depth")
        gr_infeed_dist = 0.07*self.diam + 0.18

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Radial Relief Angle", gr_rad_rel)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Axial Relief Angle", gr_ax_rel)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/dL Start", gr_dl_start)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Rotation C", gr_rot_c)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Depth", gr_depth)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Infeed Distance", gr_infeed_dist)

        # Feeds and speeds
        gr_speed = self.configuration_wb.lookup("step_relief", "diameter", self.diam, "GR_speed")
        gr_feedrate_in = self.configuration_wb.lookup("step_relief", "diameter", self.diam, "GR_feedrate_in")
        gr_feedrate = self.configuration_wb.lookup("step_relief", "diameter", self.diam, "GR_feedrate")

        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Cutting Speed", gr_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Feedrate In", gr_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Feedrate", gr_feedrate)

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
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_2")
        self.set_wheel(whp_name, 2)
        # Skip wheelpack 3
        # Load wheelpack 4
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_4")
        self.set_wheel(whp_name, 4)
        # Load wheelpack 5
        whp_name = self.configuration_wb.lookup("wheelpacks_1_5", "diameter", self.diam, "wheelpack_5")
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
        # F1
        op_wh_seg = self.configuration_wb.lookup("od_clearance", "diameter", self.diam, "F1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Wheel", op_wh_seg)

        # Set wheel segments for wheelpack 4
        # RD
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "RD_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Gash/Wheel", op_wh_seg)
        # GR
        op_wh_seg = self.configuration_wb.lookup("step_relief", "diameter", self.diam, "GR_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 1/Step 1 Step Reliefs/Wheel", op_wh_seg)

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
        coolant_text = "Attention to the coolant pipes position!!!"

        self.ds_text_args.append(coolant_text)

        # Images
        steadyrest_img_name = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "steadyrest_configuration")

        self.ds_img_names.append(steadyrest_img_name)