import numpy as np
from diagnosticsearch import NEGATIVE_SYMPTOM_VALUE, NOT_KNOWN_SYMPTOM_VALUE


class QuestionGenerator:
    def __init__(self, data_helper):
        self.data_helper = data_helper
        self.mu = 0.5
        self.c = 1

    def get_symptom_scores(self, user_symptoms, top_diagnoses):
        # Get known symptom labels
        known_symptom_labels = set()
        for idx, value in enumerate(user_symptoms):
            if value != NOT_KNOWN_SYMPTOM_VALUE:
                known_symptom_labels.add(self.data_helper.symptoms[idx])

        # Build the known symptom matrix and vector (X and y)
        user_symptoms = self._convert_to_array(user_symptoms)       # Joel: WHAT THE USER HAS CLICKED
        known_symptom_matrix, known_user_symptoms = self._filter_matrix_to_known_symptoms(user_symptoms, self.data_helper.matrix)
        known_symptom_matrix = known_symptom_matrix.T

        # Get all symptoms that are in at least one possible diagnosis (given user's symptoms)
        matching_symptom_indices = self._get_matching_symptom_indices(top_diagnoses)

        # Filter matrix to only contain symptoms that belong to some possible diagnosis
        filtered_symptoms = self.data_helper.matrix.T[sorted(matching_symptom_indices), :]
        filtered_symptom_labels = [self.data_helper.symptoms[i] for i in sorted(matching_symptom_indices)]

        # Regularization parameter
        mu = self.mu * np.eye(len(self.data_helper.diagnoses))

        # Diagnosis rank multiplier to bias the known symptom matrix
        diagnosis_rank_multiplier = self._get_diagnosis_rank_bias(top_diagnoses)

        # Bias known symptom matrix with symptom ranks
        known_symptom_matrix = known_symptom_matrix * diagnosis_rank_multiplier.T

        # Pseudo-inverse constant that stays constant for each symptom. (X'X + mu)^-1 * X'
        pinv_constant = np.linalg.solve(known_symptom_matrix.T.dot(known_symptom_matrix) + mu, known_symptom_matrix.T)

        symptom_scores = []

        # Loop over all symptoms (known and not known)
        for idx, symptom in enumerate(filtered_symptoms):
            label = filtered_symptom_labels[idx]

            # Symptoms ordinary least squares coefficients for known symptoms. s_i * (X'X + mu)^-1 * X'
            ai = symptom.dot(pinv_constant)

            # Previous feedback (binary of having or not having symptoms)
            yt = known_user_symptoms

            # OLS fit estimate given known symptoms
            ols = float(np.dot(ai, yt))

            # Exploration component, l^2 norm (euclidean norm) with adjustment factor c
            exploration = self.c / 2 * np.sqrt(np.dot(ai, ai.T))

            # Correlation component
            correlation = 0  # TODO: implement

            # Upper confidence bound
            ucb = float(ols + exploration - correlation)

            # Do not include symptoms which are already known
            if label not in known_symptom_labels:
                symptom_scores.append((label, ucb, ols, exploration, correlation))

        # Sort symptoms by score
        symptom_scores_sorted = sorted(symptom_scores, key=lambda x: x[1], reverse=True)

        return symptom_scores_sorted

    @staticmethod
    def _filter_matrix_to_known_symptoms(user_symptoms, matrix):
        # Ensure that we are not editing the original matrix
        filtered_matrix = matrix.copy()

        # Indices of all known symptoms
        users_known_symptoms_indices = np.argwhere(user_symptoms != NOT_KNOWN_SYMPTOM_VALUE).transpose()[0]

        # Pick known symptoms from user_symptoms vector
        users_known_symptom_vector = np.take(user_symptoms, users_known_symptoms_indices)

        # Change all negative symptoms (known symptoms that user doesn't have) from 0 to -1
        users_known_symptom_vector[users_known_symptom_vector == NEGATIVE_SYMPTOM_VALUE] = -1

        # Pick known symptom columns from matrix
        filtered_matrix = filtered_matrix[:, users_known_symptoms_indices]

        return filtered_matrix, users_known_symptom_vector

    @staticmethod
    def _convert_to_array(obj):
        if isinstance(obj, str):
            # vector is in form '[1, 0, 1, ...]'
            values = obj[1:-1]
            user_symptoms = np.fromstring(values, dtype=int, sep=' ')
        elif isinstance(obj, list):
            user_symptoms = np.array(obj)
        else:
            raise TypeError('User symptom vector is in unrecognizable type')
        return user_symptoms

    def _get_matching_symptom_indices(self, top_diagnoses):
        matching_symptoms = set()
        for diagnosis, _, _, _ in top_diagnoses:
            diagnosis_symptoms = self.data_helper.get_diagnoses_symptoms(diagnosis)
            matching_symptoms = matching_symptoms.union(diagnosis_symptoms)

        matching_indices = [self.data_helper.symptoms.index(symptom) for symptom in matching_symptoms]

        return matching_indices

    def _get_diagnosis_rank_bias(self, top_diagnoses):
        diagnosis_multiplier = np.ones(shape=(len(self.data_helper.diagnoses), 1))

        for rank, diagnosis in enumerate(top_diagnoses):
            diagnosis_label, weight, _, _ = diagnosis
            diagnosis_index = self.data_helper.diagnoses.index(diagnosis_label)

            # Harmonic decay with multiplier
            m = 10
            diagnosis_multiplier[diagnosis_index] += m/(rank + 1)

        return diagnosis_multiplier
