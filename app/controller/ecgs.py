# Controller for the ecg model

class EcgService:
    def __init__(self, ecgs_service=None):
        self.ecgs_service = ecgs_service

    def calculate_zero_crossings(self, leads):
        return sum(
            1 for lead in leads
            for i in range(1, len(lead.signal))
            if lead.signal[i - 1] < 0 and lead.signal[i] >= 0
        )


# Singleton instance
egs_service = EcgService()
