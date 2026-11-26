
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            age = int(request.form["age"])
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            systolic = int(request.form["systolic"])
            diastolic = int(request.form["diastolic"])
            exercise = int(request.form["exercise"])
            sleep = float(request.form["sleep"])
            sitting = int(request.form["sitting"])

            if not 18 <= age <= 110:
                raise ValueError("Enter an age between 18 and 110.")
            if not 120 <= height <= 230 or not 25 <= weight <= 300:
                raise ValueError("Check your height and weight.")
            if not 60 <= systolic <= 260 or not 30 <= diastolic <= 160:
                raise ValueError("Check your blood pressure values.")
            if systolic <= diastolic:
                raise ValueError("Systolic pressure must exceed diastolic pressure.")
            if not 0 <= exercise <= 7 or not 0 <= sleep <= 24:
                raise ValueError("Check exercise or sleep hours.")
            if not 0 <= sitting <= 24:
                raise ValueError("Check sitting hours.")

            bmi = weight / ((height / 100) ** 2)

            factors = []
            suggestions = []

            def add_factor(message, advice):
                factors.append(message)
                suggestions.append(advice)

            if systolic >= 140 or diastolic >= 90:
                add_factor(
                    "High blood pressure reading",
                    "Arrange a blood pressure review with a healthcare professional."
                )
            elif systolic >= 130 or diastolic >= 80:
                add_factor(
                    "Blood pressure above preferred range",
                    "Track your readings and discuss them with a healthcare professional."
                )

            if bmi >= 30:
                add_factor(
                    "BMI in obesity range",
                    "Discuss sustainable nutrition and activity goals with a professional."
                )
            elif bmi >= 25:
                add_factor(
                    "BMI in overweight range",
                    "Focus on sustainable healthy habits. BMI is only a screening measure."
                )

            if request.form["cholesterol"] == "high":
                add_factor(
                    "High cholesterol reported",
                    "Discuss cholesterol testing and management with your clinician."
                )

            if request.form["glucose"] == "high":
                add_factor(
                    "High glucose reported",
                    "Discuss blood glucose testing and follow-up with your clinician."
                )

            if request.form["diabetes"] == "yes":
                add_factor(
                    "Diabetes reported",
                    "Follow your healthcare professional's diabetes management plan."
                )

            if request.form["smoking"] == "yes":
                add_factor(
                    "Smoking reported",
                    "Consider quitting tobacco with professional support."
                )

            if request.form["family"] == "yes":
                add_factor(
                    "Family history of heart disease",
                    "Share your family history with your healthcare professional."
                )

            if exercise < 3:
                add_factor(
                    "Low number of active days",
                    "Gradually increase safe physical activity."
                )

            if sleep < 7:
                add_factor(
                    "Insufficient sleep duration",
                    "Try maintaining a regular sleep routine."
                )

            if sitting >= 8:
                add_factor(
                    "Long sitting duration",
                    "Take regular movement breaks during the day."
                )

            if request.form["diet"] == "poor":
                add_factor(
                    "Frequent unhealthy food choices",
                    "Include more vegetables, fruits, whole grains and beans."
                )

            if request.form["stress"] == "high":
                add_factor(
                    "High stress reported",
                    "Try relaxation activities and seek support when needed."
                )

            if request.form["alcohol"] == "often":
                add_factor(
                    "Frequent alcohol consumption",
                    "Consider reducing alcohol and discussing it with a professional."
                )

            if not suggestions:
                suggestions.append(
                    "Continue balanced meals, regular movement, adequate sleep "
                    "and routine health check-ups."
                )

            # This is a transparent checklist category,
            # NOT a medically validated risk score.
            count = len(factors)

            if count <= 2:
                category = "Fewer factors flagged"
                level = "low"
            elif count <= 5:
                category = "Some factors need attention"
                level = "moderate"
            else:
                category = "Multiple factors need attention"
                level = "high"

            emergency = (
                request.form["chest"] == "yes"
                or request.form["breathing"] == "yes"
                or request.form["fainting"] == "yes"
            )

            if emergency:
                category = "Urgent symptoms reported"
                level = "urgent"

            result = {
                "category": category,
                "level": level,
                "bmi": round(bmi, 1),
                "factors": factors,
                "suggestions": suggestions,
                "emergency": emergency
            }

        except ValueError as error:
            result = {"error": str(error)}

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
