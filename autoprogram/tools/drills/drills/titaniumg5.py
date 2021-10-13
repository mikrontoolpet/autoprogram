from pathlib import Path
import math
from autoprogram.tools.common import BaseTool
from autoprogram.wbhandler import WorkBook

class Tool(BaseTool):
    """
    Titanium drill class
    """
    """
    The class variable "family_address" is necessary and must be equal
    to both:
    1) The relative path between the master programs base directory and the
       master program directory itself
    2) The relative module path between the module "tools" and this class
    """
    family_address = "drills/drills/titaniumg5"

    def __init__(self, vgp_client, name, diam, fl_len, lead):
        super().__init__(vgp_client, name, Tool.family_address) # update class name here too!
        self.diam = float(diam)
        self.fl_len = float(fl_len)
        self.lead = float(lead)
        self.configuration_wb = WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/TitaniumG5/configuration_file.xlsx")

        # Check the input parameters boundary
        self.check_boundary(self.diam, 1, 6.35)
        self.check_boundary(self.fl_len, 6*self.diam, 20*self.diam)

    async def set_parameters(self):
        # Margin calculations
        # Circular land width varies along the flute length
        # land_width_1 = 0.07*self.diam
        # land_width_2 = 0.07*self.diam
        # f_wh_width = float(WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/drills/drills/Titanium/configuration_file.xlsx").lookup("whp_4", "diam", self.diam, "f_wh_width")) # formatted as float to make calculations
        # rel_width = circ_land_width - land_width_1 - land_width_2
        # marg_width_1 = land_width_1 # program parameter to create the first land width
        # marg_width_101 = marg_width_1 + rel_width - f_wh_width # program parameter to create the second land width

        # Set parameters
        # Set 1
        # Common Data
        await self.vgpc.set("ns=2;s=tool/Tool/Reference Length (RL)", 0.75*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/End Stock Removal (dL)", 0.0579*self.diam + 0.0342)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Cutting Security Distance", 0.1685*self.diam + 0.1331)
        delta_dl = await self.vgpc.get("ns=2;s=tool/Tool/Set 1/Delta dL (Output)")

        # Profile
        point_ang = 140
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/pA", point_ang)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/D0", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/Ta0", -0.0286)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Profile/sP1", self.fl_len - 1.833*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Straightness Diameter", 27)
        point_len = self.diam/2*math.tan(math.radians(90 - point_ang/2))

        # Flute 1
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length", self.fl_len - 0.25*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Lead", self.lead)

        # Flute 1 (G1)
        # Core diameter, rake angle and circular land width have a transition in values along the flute length
        g1_trans_len = 5*self.diam
        g1_len = await self.vgpc.get("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute Length")
        g1_trans_perc = (g1_trans_len - point_len)/(g1_len - point_len)*100
        g1_core_diam_perc_1 = 32
        g1_core_diam_perc_2 = 27
        g1_rake_ang_1 = 16
        g1_rake_ang_2 = 19
        g1_circ_land_width_1 = 0.8*self.diam
        g1_circ_land_width_2 = 0.75*self.diam
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter Definition", "[in %];in mm")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Core Diameter", "(s1;0%;" + str(g1_core_diam_perc_1) + "%);(s1;" + str(g1_trans_perc) + "%;" + str(g1_core_diam_perc_2) + "%);(s1;100%;" + str(g1_core_diam_perc_2) + "%)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Fluting Shape", "Edge Straightness;Chisel Distance;[Rake Angle];Attack Angle")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Rake Angle", "(s1;0%;" + str(g1_rake_ang_1) + "°);(s1;" + str(g1_trans_perc) + "%;" + str(g1_rake_ang_2) + "°);(s1;100%;" + str(g1_rake_ang_2) + "°)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Measure Distance", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Circular Land Width", "(s1;0%;" + str(g1_circ_land_width_1) + " mm);(s1;" + str(g1_trans_perc) + ";" + str(g1_circ_land_width_2) + " mm);(s1;100%;" + str(g1_circ_land_width_2) + " mm)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/dL Start", 0.0374*self.diam + 0.1126)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Exit Radius", 0.25*self.diam)
        # Feedrates
        g1_feedrate_in = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_feedrate_in")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate In", g1_feedrate_in)
        g1_feedrate = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Feedrate", g1_feedrate)

        # Flute 101 (S_G1)
        s_g1_rad_stk_rmv_perc = 2.5 # percent of diameter
        s_g1_rad_stk_rmv = s_g1_rad_stk_rmv_perc*self.diam/100
        s_g1_trans_perc = g1_trans_perc
        s_g1_core_diam_perc_1 = g1_core_diam_perc_1 + 2*s_g1_rad_stk_rmv_perc
        s_g1_core_diam_perc_2 = g1_core_diam_perc_2 + 2*s_g1_rad_stk_rmv_perc
        rake_ang_diff = 4
        s_g1_rake_ang_1 = g1_rake_ang_1 - rake_ang_diff
        s_g1_rake_ang_2 = g1_rake_ang_2 - rake_ang_diff
        s_g1_circ_land_width_1 = g1_circ_land_width_1 + s_g1_rad_stk_rmv
        s_g1_circ_land_width_2 = g1_circ_land_width_2 + s_g1_rad_stk_rmv
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Shift", -s_g1_rad_stk_rmv)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter Definition", "[in %];in mm")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Core Diameter", "(s1;0%;" + str(s_g1_core_diam_perc_1) + "%);(s1;" + str(s_g1_trans_perc) + "%;" + str(s_g1_core_diam_perc_2) + "%);(s1;100%;" + str(s_g1_core_diam_perc_2) + "%)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Fluting Shape", "Edge Straightness;Chisel Distance;[Rake Angle];Attack Angle")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Rake Angle", "(s1;0%;" + str(s_g1_rake_ang_1) + "°);(s1;" + str(s_g1_trans_perc) + "%;" + str(s_g1_rake_ang_2) + "°);(s1;100%;" + str(s_g1_rake_ang_2) + "°)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Circular Land Width", "(s1;0%;" + str(s_g1_circ_land_width_1) + " mm);(s1;" + str(s_g1_trans_perc) + "%;" + str(s_g1_circ_land_width_2) + " mm);(s1;100%;" + str(s_g1_circ_land_width_2) + " mm)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL Start", 0.0374*self.diam + 0.1126)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/dL End", 0.075*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Exit Radius", 0.25*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Infeed Down Y", 0.04*self.diam + 0.06)
        # Feedrates
        s_g1_feedrate_in = self.configuration_wb.lookup("whp_1", "diam", self.diam, "S_G1_feedrate_in")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate In", s_g1_feedrate_in)
        s_g1_feedrate = self.configuration_wb.lookup("whp_1", "diam", self.diam, "S_G1_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Feedrate", s_g1_feedrate)

        # Flute 201 (RN)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Rake Shift", 0.0166*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Core Diameter Definition", "[in %];in mm")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Core Diameter", 75)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Attack Angle", 30)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL Start", -5.033*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/dL End", -0.5*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Exit Radius", 0.1*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Infeed Down Y", 0.04*self.diam + 0.06)

        # Flute 301 (ERF)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Rake Shift", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Core Diameter Definition", "[in %];in mm")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Core Diameter", 75)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Attack Angle", 30)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Wheel Displacement", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/dL Start", -2.5*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/dL End", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Infeed Down Y", 0.5*self.diam)

        #Flute 1001 (G2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Connection Point", "s0;90%")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Flute Length", 5.633*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Lead", self.lead)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Core Diameter Definition", "[in %];in mm")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Core Diameter", 52.5)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Rake Angle", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Measure Distance", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Circular Land Width", round(1.03*self.diam, 3))
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL Start", 0.0374*self.diam + 0.1126)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/dL End", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Exit Radius", 0.1*self.diam)
        # Feedrates
        g2_feedrate_in = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G2_feedrate_in")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Feedrate In", g2_feedrate_in)
        g2_feedrate = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G2_feedrate")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Feedrate", g2_feedrate)

        # Step 0
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Calculation Mode", "[Automatic];Manual")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Follow Operations/Flute 1", "[True];False")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Follow Operations/Flute 1001", "[True];False")
        # chisel_dist = await self.vgpc.get("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Chisel Distance (Output)") # empty value during calculations!
        # edge_angle = math.atan(chisel_dist/(self.diam/2))

        # Gash (TN1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Rotation", 0.5*self.diam - 6)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Web Thickness", 0.113*self.diam + 0.006)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Gash Angle", 58)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Rake Angle", 15)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Depth Past Center Yp", -0.22*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Angle", 90)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Length", 0.05)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Type", "None;[Straight];Radius;Custom")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Length", 0.05)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Sweep Angle", 90)

        # # S-Gash (SS)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Rotation", 30)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Web Thickness", -0.009*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Gash Angle", 58)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Rake Angle", -0.2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Depth Past Center Yp", -0.065*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Radius", 0.175*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle Correction", 4)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Chisel Distance Correction", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sR", 0.0866*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sA", 96)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Profile 2D/sL", 0.17*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Exit Angle", 65)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/S-Gash/Walk Coefficient", 30)

        # Point Relief
        # Relief 1
        # Point Relief 1 (P1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Type", "[Flat];Conical;Straight (automatic A and Gp)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Angle Measurement Method", "[Parallel to Z];Normal to Profile;Radial and axial")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Relief Angle", 16)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL Start", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/dL End", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Direction of Grinding Marks", 0)
        # Point Relief 2 (P2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Type", "[Flat];Conical;Straight (automatic A and Gp)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Angle Measurement Method", "[Parallel to Z];Normal to Profile;Radial and axial")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Relief Angle", 30)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL Start", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/dL End", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Direction of Grinding Marks", 0)
        # Relief 101
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Stock Removal", 0.05)
        # Point Relief 102 (SGR P2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Type", "[Flat];Conical;Straight (automatic A and Gp)")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Angle Measurement Method", "[Parallel to Z];Normal to Profile;Radial and axial")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Relief Angle", 30)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL Start", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/dL End", 0.1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Direction of Grinding Marks", 0)

        # Step 0 Diameter
        # Step 0 OD Clearance
        # OD Clearance 1 (F1)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Margin Width", 0.095*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Back Clearance", 95)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Setting Angle", 40)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Drop Angle", 3)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/dL Start", 0.2)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/dL End", 0)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/C Rotation at end", 35)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Rotation C axial angle", 0)

        # Set 2
        # OD Profile 2D
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Radius", 0.15*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Angle_in", 30)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Length", 0.15*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Angle_out", 50)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter_in", 0.27*self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Diameter_out", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/OD Profile 2D/Length_in", 0.15*self.diam)

        # Gash 1 (No)
        gash_index = self.configuration_wb.trend("others", "diam", self.diam, "AF_index")
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Index", gash_index)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/D", self.diam)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 2/Rake Operations/Gash 1/Virtual Profile/dD", 0.3)

        # Set 3
        # Peeling Operation 1 (ERT)
        await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Blank Preparation 1/Peeling Operation/Custom Profile/PS", -0.75*self.diam)

        # Blank
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/D", self.diam)
        await self.vgpc.set("ns=2;s=tool/Blank/Profile/L", self.fl_len + 0.5*self.diam)

    async def set_wheels(self):
        pass
    #     # Load wheelpacks and set wheel segments
    #     # Load wheelpack 1
    #     # whp_name = self.configuration_wb.lookup("whp_1", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 1)
    #     # Set wheel segments for wheelpack 1
    #     # S_G1
    #     op_wh_seg = self.configuration_wb.lookup("whp_1", "diam", self.diam, "S_G1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 101/Wheel", op_wh_seg)
    #     # RN
    #     op_wh_seg = self.configuration_wb.lookup("whp_1", "diam", self.diam, "RN_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 201/Wheel", op_wh_seg)

    #     # Load wheelpack 2
    #     # whp_name = self.configuration_wb.lookup("whp_2", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 2)
    #     # Set wheel segments for wheelpack 2
    #     # TN1
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "TN1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Wheel", op_wh_seg)
    #     # SS
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "SS_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Gash/Wheel", op_wh_seg)
    #     # P1
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "P1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 1/Wheel", op_wh_seg)
    #     # P2
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "P2_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 1/Point Relief 2/Wheel", op_wh_seg)
    #     # S_P2
    #     op_wh_seg = self.configuration_wb.lookup("whp_2", "diam", self.diam, "S_P2_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Point Relief/Relief 101/Point Relief 102/Wheel", op_wh_seg)

    #     # Load wheelpack 4
    #     # whp_name = self.configuration_wb.lookup("whp_4", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 4)
    #     # Set wheel segments for wheelpack 4
    #     # F1
    #     op_wh_seg = self.configuration_wb.lookup("whp_4", "diam", self.diam, "F1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Step 0 (Point)/Step 0 Diameter/Step 0 OD Clearance/Wheel", op_wh_seg)

    #     # Load wheelpack 5
    #     # whp_name = self.configuration_wb.lookup("whp_5", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 5)
    #     # Set wheel segments for wheelpack 5
    #     # ERF
    #     op_wh_seg = self.configuration_wb.lookup("whp_5", "diam", self.diam, "ERF_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 301/Wheel", op_wh_seg)
    #     # ERT
    #     op_wh_seg = self.configuration_wb.lookup("whp_5", "diam", self.diam, "ERT_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 3/Blank Preparation 1/Peeling Operation/Peeling Operation 1/Wheel", op_wh_seg)
        
    #     # # Load wheelpack 6
    #     # whp_name = self.configuration_wb.lookup("wheels", "diam", self.diam, "whp_name")
    #     # whp_path = Path(config.STD_WHP_BASE_DIR).joinpath(whp_name + config.WHP_SUFFIX)
    #     # await self.vgpc.load_wheel(whp_path, 6)
    #     # Set wheel segments for wheelpack 6
    #     # G1
    #     op_wh_seg = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1/Flute 1 (Output)/Wheel", op_wh_seg)
    #     # G2
    #     op_wh_seg = self.configuration_wb.lookup("whp_6", "diam", self.diam, "G1_wheel")
    #     await self.vgpc.set("ns=2;s=tool/Tool/Set 1/Common Data/Flutes/Flute 1001/Wheel", op_wh_seg)