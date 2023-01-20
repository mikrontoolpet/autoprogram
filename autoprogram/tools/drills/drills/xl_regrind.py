from pathlib import Path
import math
from autoprogram.tools.basetool import BaseTool
from autoprogram.wbhandler import WorkBook


class Tool(BaseTool):
    """
    CrazyDrill XL 
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/drills/xl_regrind"
    machine = "R628XW"

    def __init__(self, vgp_client, name, diameter):
        super().__init__(vgp_client, name) # update class name here too!
        self.diam = float(diameter)

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1.4, 6.4)

    async def set_parameters(self):

        end_stk_rmv = self.common_wb.lookup("end_stock", "diameter", self.diam, "end_stock")

        #blank
        self.set("ns=2;s=tool/Blank/Profile/D", self.diam)
        self.set("ns=2;s=tool/Blank/Profile/L", self.diam*11)

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
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", self.diam)
        tip_angle = self.configuration_wb.lookup("function_data", "diameter", self.diam, "tip_angle")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", tip_angle)

        #  # Flute 1 (G1)
        lead = self.configuration_wb.lookup("blank", "diameter", self.diam, "lead")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", lead)
        G1_attack_angle = self.configuration_wb.trend("function_data", "diameter", self.diam, "G1_attack_angle")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Attack Angle", G1_attack_angle)
        

        #  # Flute 1001 (G2)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", lead)
        G2_attack_angle = self.configuration_wb.trend("function_data", "diameter", self.diam, "G2_attack_angle")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Attack Angle", G2_attack_angle)
        flute_connection = self.configuration_wb.lookup("function_data", "diameter", self.diam, "flute_connection")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Connection Point", flute_connection)

        # S-Gash
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.225*self.diam)
        chisel_distance = self.configuration_wb.lookup("function_data", "diameter", self.diam, "chisel_distance")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Chisel Distance Correction", chisel_distance)
        # Feeds and speeds
        S_Gash_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_speed")
        S_Gash_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate_in")
        S_Gash_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_feedrate")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Cutting Speed", S_Gash_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feedrate In", S_Gash_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Feedrate", S_Gash_feedrate)

        # TN1
        TN1_X = self.configuration_wb.trend("function_data", "diameter", self.diam, "TN1_X")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", TN1_X)
        gash_rotation = self.configuration_wb.trend("function_data", "diameter", self.diam, "gash_rotation")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", gash_rotation)
        # Feeds and speeds
        tn1_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_speed")
        tn1_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate_in")
        tn1_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_feedrate")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Cutting Speed", tn1_speed)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Feedrate In", tn1_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Feed along sweep+exit", tn1_feedrate)

        
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
        

        # Set 2
        # Profile
        self.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter", self.diam)
        length_SM = self.configuration_wb.trend("function_data", "diameter", self.diam, "length_SM")
        self.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Distance", length_SM)

        # Feeds and Speeds
        sm_speed = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_speed")
        sm_feedrate_in = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_feedrate_in")
        sm_feedrate = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_feedrate")
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Cutting Speed", sm_speed)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate In", sm_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Feedrate", sm_feedrate)

        

        # Set 3
        # Profile
        self.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Diameter", self.diam)
        length_SM = self.configuration_wb.trend("function_data", "diameter", self.diam, "length_SM")
        self.set("ns=2;s=tool/Tool/Set 3/OD Profile 2D/Distance", length_SM)

        # TN2
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/D", 1.17*self.diam)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/dD", 0.943*self.diam)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Virtual Profile/dZ", -(0.168*self.diam))
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Profile 2D/sR", 0.323*self.diam)
        Index = self.configuration_wb.trend("function_data", "diameter", self.diam, "Index")
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Index", Index)
        web_thick = self.configuration_wb.trend("function_data", "diameter", self.diam, "web_thick")
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Web Thickness", web_thick)
        # Feeds and speeds
        tn2_speed = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_speed")
        tn2_feedrate_in = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate_in")
        tn2_feedrate = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_feedrate")
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Cutting Speed", tn2_speed)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Feedrate In", tn2_feedrate_in)
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Feed along sweep+exit", tn2_feedrate)

    def set_wheels(self):
        """
        Load wheelpacks and set wheel segments
        """
        # Load wheelpack 1
        whp_name = self.configuration_wb.lookup("wheelpacks", "diameter", self.diam, "wheelpack_1")
        self.set_wheel(whp_name, 1)
        # Load wheelpack 2
        whp_name = self.configuration_wb.lookup("wheelpacks", "diameter", self.diam, "wheelpack_2")
        self.set_wheel(whp_name, 2)
        # Skip wheelpack 3
        # Skip wheelpack 4
        # Skip wheelpack 5
        # Load wheelpack 6
        whp_name = self.configuration_wb.lookup("wheelpacks", "diameter", self.diam, "wheelpack_6")
        self.set_wheel(whp_name, 6)

    def set_wheel_segments(self):
        # # Set wheel segments for wheelpack 1
        # # G1
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Straight Gash/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "TN2_wheel")
        self.set("ns=2;s=tool/Tool/Set 3/Rake Operations/Gash 1/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("gashes", "diameter", self.diam, "SS_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Wheel", op_wh_seg)
        

        # # Set wheel segments for wheelpack 2
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "P2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("point_relieves", "diameter", self.diam, "S_P2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)
        op_wh_seg = self.configuration_wb.lookup("SM", "diameter", self.diam, "SM_wheel")
        self.set("ns=2;s=tool/Tool/Set 2/Reliefs/Relief Section 1/Relief 1/Wheel", op_wh_seg)

        # # Set wheel segments for wheelpack 4

        # # Set wheel segments for wheelpack 5

        # # Set wheel segments for wheelpack 6
        # G1
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G1_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Wheel", op_wh_seg)
        # G2
        op_wh_seg = self.configuration_wb.lookup("polishing_flutes", "diameter", self.diam, "G2_wheel")
        self.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Wheel", op_wh_seg)
        

    def set_isoeasy(self):
        """
        Set isoeasy
        """
        self.isoeasy_name = self.configuration_wb.lookup("isoeasy", "diameter", self.diam, "isoeasy_name")

    def set_datasheet(self):
        # Arobotech gripper length
        ar_support_len = self.configuration_wb.lookup("datasheet", "diameter", self.diam, "arobotech_gripper_length")
        support_len_text = "Arobotech support length: " + str(ar_support_len) + " mm"
        self.ds_text_args.append(support_len_text)