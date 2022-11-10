###################################################################
#                                                                 #
#     Contains functions for parsing input parameters for sim     #
#                                                                 #
###################################################################

class PsychoInput:

    def __init__(self, input_fname: str):

        self.input_fname = input_fname

        # Dictionary containing all problem information
        self.value_dict = dict()

    def parse_input_file(self):
        """
        Loops through parameter file and stores values from file
        to be used in problem generator
        """

        with open(self.input_fname) as f:

            # Strip all of spcaes surrounding strings of interest
            lines = (line.rstrip() for line in f)
            lines = (line for line in lines if line)

            # Loop through lines in the problem file
            for line in lines:

                # Ignore comment lines
                if not line.startswith("#"):
                    key = line.split("=")[0].strip()
                    val = line.split("=")[1].strip()

                    # Numbers with `.` are stored as floats, otherwise ints
                    if "." in val:
                        self.value_dict[key] = float(val)
                    else:
                        self.value_dict[key] = int(val)
