from flask import Flask, request, Response
from utils.credit_card import CreditCard
from utils import helpers
import logging

app = Flask(__name__)

ERROR_200 = "Payment is processed"
ERROR_400 = "Request is invalid"
ERROR_500 = "Internal server error"


@app.route('/ProcessPayment', methods=['POST'])
def process_payment():
    try:
        request_body = request.json

        cc_number = str(request_body.get("CreditCardNumber", ''))
        cc_holder = str(request_body.get("CardHolder", ''))
        cc_exp = str(request_body.get("ExpirationDate", ''))
        cc_cvc = str(request_body.get("SecurityCode", ''))
        cc_amt = float(request_body.get("Amount", '0'))

        month, year = helpers.get_month_year(cc_exp)

        if cc_number and cc_holder and month and year and cc_amt:
            cc = CreditCard(
                number=cc_number,
                month=month,
                year=year,
                cvc=cc_cvc,
                holder=cc_holder
            )

            if cc.is_valid and cc.is_cvc_valid:
                payment_processed = False
                payment_error = ''
                if cc_amt >= 0 and cc_amt <= 20:
                    # CheapPaymentGateway 
                    payment_processed = True 
                elif cc_amt > 20 and cc_amt <= 500:
                    # ExpensivePaymentGateway or CheapPaymentGateway
                    payment_processed = True
                elif cc_amt > 500:
                    # PremiumPaymentGateway(retry=3)
                    payment_processed = True
                else:
                    payment_error = "Amount is invalid"

                if payment_processed:
                    return Response(ERROR_200, status=200, mimetype='application/json')
                else:
                    logging.error(payment_error)
                    return Response(ERROR_400, status=400, mimetype='application/json')
            else:
                logging.error("Not Valid : Credit Card/CVC")
                return Response(ERROR_400, status=400, mimetype='application/json')
        else:
            logging.error("Mandatory fileds missing")
            return Response(ERROR_400, status=400, mimetype='application/json')
    except ValueError as ve:
        logging.error(ve)
        return Response(ERROR_400, status=400, mimetype='application/json')
    except Exception as e:
        logging.error(e)
        return Response(ERROR_500, status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
