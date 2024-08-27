from flask import jsonify, make_response, abort


def populate_object(obj, data_dictionary):
    fields = data_dictionary.keys()

    for field in fields:
        try:
            getattr(obj, field)
            setattr(obj, field, data_dictionary[field])

        except AttributeError:
            response = make_response(jsonify({"message": "atribute not in obj"}), 400)
            abort(response)

        except Exception as e:
            response = make_response(jsonify({"message": e}), 400)
            abort(response)
