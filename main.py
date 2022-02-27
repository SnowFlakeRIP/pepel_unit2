import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, math


class server(BaseHTTPRequestHandler):

    def do_POST(self):
        def end_response(self, response):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        # получение длины нагрузки
        length = int(self.headers['Content-length'])
        if self.path == '/math':
            # получение json строки
            post_data = self.rfile.read(length)
            data = post_data.decode('utf-8')
            data = json.loads(data)
            try:
                first_index = data["a"]
                second_index = data["b"]
                free_index = data["c"]
                if type(first_index) == str or type(second_index) == str or type(free_index) == str:
                    type_error = {
                        "error": "Один из аргументов не является числом"
                    }
                    end_response(self, type_error)
                first_index = float(first_index)
                second_index = float(second_index)
                free_index = float(free_index)
                discr = second_index ** 2 - 4 * first_index * free_index
                answers = []
                if discr > 0:
                    x1 = (-second_index + math.sqrt(discr)) / (2 * first_index)
                    x2 = (-second_index - math.sqrt(discr)) / (2 * first_index)
                    answers.append(x1)
                    answers.append(x2)
                    response = {
                        "Дискриминант": discr,
                        "Ответ": answers
                    }
                    end_response(self, response)
                    answers.clear()
                elif discr == 0:
                    x = -second_index / (2 * first_index)
                    answers.append(x)
                    response = {
                        "Дискриминант": discr,
                        "Ответ": answers
                    }
                    end_response(self, response)
                    answers.clear()
                else:
                    response = {
                        "message": "Корней нет"
                    }
                    end_response(self, response)
            except:
                error = {
                    "error": "Что-то пошло не так"
                }
                end_response(self, error)
        elif self.path == '/random':
            try:
                elements_dict = {1: 'Камень', 2: 'Ножницы', 3: 'Бумага'}
                random_int = random.randint(1, 3)
                server_answer = elements_dict.get(random_int)
                print(f"Ответ сервера: {server_answer}")
                post_data = self.rfile.read(length)
                data = post_data.decode('utf-8')
                data = json.loads(data)
                user_query = data["user"]
                print(len(user_query.capitalize()))
                print(len(user_query.capitalize().strip()))
                print(user_query.capitalize().strip() in elements_dict.values())
                if (user_query.capitalize().strip() in elements_dict.values()) == False:
                    response = {
                        "result": f"Я в такое не умею введите что-то из этого: {(elements_dict.values())}"
                    }
                    end_response(self, response)
                elif server_answer == user_query.capitalize().strip():
                    response = {
                        "server_result": server_answer,
                        "result": "Ничья, го еще разок"
                    }
                    end_response(self, response)
                elif (server_answer == 'Камень' and user_query.capitalize().strip() == 'Ножницы') or (
                        server_answer == 'Ножницы' and user_query.capitalize().strip() == 'Бумага') or (
                        server_answer == 'Бумага' and user_query.capitalize().strip() == 'Камень'):
                    response = {
                        "server_result": server_answer,
                        "result": "ЛОХ, СИДР"
                    }
                    end_response(self, response)
                elif (server_answer == 'Ножницы' and user_query.capitalize().strip() == 'Камень') or (
                        server_answer == 'Камень' and user_query.capitalize().strip() == 'Бумага') or (
                        server_answer == 'Бумага' and user_query.capitalize().strip() == 'Ножницы'):
                    response = {
                        "server_result": server_answer,
                        "result": "В этот раз тебе повезло, собака сутулая"
                    }
                    end_response(self, response)
            except:
                error = {
                    "error": "Что-то пошло не так"
                }
                end_response(self, error)
        elif self.path == '/save_file':
            try:
                post_data = self.rfile.read(length)
                data = post_data.decode('utf-8')
                data = json.loads(data)
                user_text = data["text"]
                file = open("text.txt", "w+")
                file.write(user_text)
                server_text = file.read()
                response = {
                    "result": "Запись прошла успешно"
                }
                end_response(self, response)
                file.close()
            except:
                response = {
                    "result": "Что-то пошло не так"
                }
                end_response(self, response)


httpd = HTTPServer(('localhost', 8001), server)
httpd.serve_forever()
