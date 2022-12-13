###################################################################
#                                                                 #
#     Contains functions for parsing input parameters for sim     #
#                                                                 #
###################################################################


class PsychoInput:
    """Class containing the input information

    Parameters
    ----------
    input_fname : str
        The name of the input file

    Attributes
    ----------
    input_fname : str
        The name of the input file

    value_dict : dict
        Dictionary containing the problem input
        information (after parsing the input file)

    """

    def __init__(self, input_fname: str):

        self.input_fname = input_fname

        # Dictionary containing all problem information
        self.value_dict = dict()

    def parse_input_file(self) -> None:
        """Parses and stores information from input file

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
                    elif (
                        key == "left_bc"
                        or key == "right_bc"
                        or key == "top_bc"
                        or key == "bottom_bc"
                        or key == "stability_name"
                        or key == "output_variables"
                        or key == "output_frequency"
                        or key == "data_file_type"
                    ):
                        self.value_dict[key] = str(val)
                    elif (
                        key == "output_variables"
                        or key == "variables_to_plot"
                        or key == "labels"
                        or key == "cmaps"
                    ):
                        val = val.strip("[]")
                        self.value_dict[key] = [str(var) for var in val.split(",")]
                    elif key == "style_mode":
                        self.value_dict[key] = eval(val)
                    else:
                        self.value_dict[key] = int(val)
