from scipy.stats import linregress


class Result:
    # Class for converting a raw .itc file into a graphable result
    @staticmethod
    def string_to_float(string) -> float:
        split_string = string.split()
        value = float(split_string[1])
        return value

    @staticmethod
    def find_list_average(lst, start, end, index) -> float:
        avg = sum(float(i[index]) for i in lst[start:end]) / len(lst[start:end])
        return avg

    @staticmethod
    def plot_concentration(sizes, concentration) -> list:
        concentration_list = [0]
        for n in range(0, len(sizes)):
            concentration_list.append(sizes[n] * concentration + concentration_list[n])
        return concentration_list

    # Handle calculation of average heat rates, data set and number of injections as input
    def find_heat_rate(self, data, n) -> list:
        injection_indices = []
        injection_lengths = []
        average_heats = [0]
        # Find injection locations in data
        for i in range(1, n + 1, 1):
            for line in data:
                if f'@{i}' in line[0]:
                    injection_lengths.append(int(float(line[3])))
                    injection_indices.append(data.index(line) + 1)
        # Add virtual "last" injection
        injection_indices.append(len(data) + 1)
        # Calculate baseline
        self.baseline = self.find_list_average(data, injection_indices[1] - 61, injection_indices[1] - 1, 1) * 4.184
        # Calculate average heat rates of injections
        for i in range((2 if self.ignore_first else 1), n + 1, 1):
            average_heats.append(
                4.184 * (self.find_list_average(data, injection_indices[i] - 61, injection_indices[i] - 1, 1)) -
                self.baseline)
        return average_heats

    def find_xy(self):
        number_of_injections = 0
        # Define beginning of injection table
        for line in self.data:
            if 'ADC' in line[0]:
                injection_index = self.data.index(line) + 2

        # Create arrays containing injection volumes and spacings
        for line in self.data[injection_index:]:
            # Find end of injection table
            if "# 0" in line[0]:
                break
            if self.ignore_first:
                if number_of_injections > 0:
                    self.injection_sizes.append(self.string_to_float(line[0]))
                    self.injection_spacings.append(int(line[2]))
                number_of_injections += 1
            else:
                self.injection_sizes.append(self.string_to_float(line[0]))
                self.injection_spacings.append(int(line[2]))
                number_of_injections += 1
        self.y = self.find_heat_rate(self.data, number_of_injections)
        self.x = self.plot_concentration(self.injection_sizes, 1)

        # Perform linear fit
        fit = linregress(self.x, self.y)
        self.fit_x = [0, self.x[-1]]
        self.fit_y = [fit.intercept, self.fit_x[-1] * fit.slope + fit.intercept]
        self.slope = fit[0]
        self.rsquared = fit[2]

    def __init__(self, name, data, ignore_boolean, color):
        self.name = name
        self.data = data
        self.color = color
        self.ignore_first = ignore_boolean
        self.injection_spacings = []
        self.injection_sizes = []
        self.baseline = 0
        self.slope = 0
        self.rsquared = 0
        self.x = []
        self.y = []
        self.fit_x = []
        self.fit_y = []
        # Everything else has to be before find_xy()
        self.find_xy()
