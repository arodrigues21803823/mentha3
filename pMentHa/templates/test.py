def fazPrimeiraPergunta(request, testID, patientID):
    """Esta função é chamada quando na tabela se inicia um teste """
    question = QuestionOrder.objects.get(test=testID, order=1).question
    options = Option.objects.filter(question=question.id)
    patientInstance = Patient.objects.get(pk=patientID)
    testInstance = Test.objects.get(pk=testID)
    resolution = resolution_exists(patientInstance, testInstance)
    if resolution:
        answer = Answer.objects.filter(question=question.id,
                                       resolution=Resolution.objects.get(test=testInstance,
                                                                         patient=patientInstance))
        if answer:
            answer = Answer.objects.get(question=question.id,
                                        resolution=Resolution.objects.get(test=testInstance,
                                                                          patient=patientInstance)).text
            resolution = Resolution.objects.get(patient=patientInstance, test=testInstance)
            if question.multipla:
                print(question.cover)
                if question.cover:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "options": options,
                        "answer": int(answer),
                        "order": 1,
                        "image": question.cover,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
                else:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "options": options,
                        "answer": int(answer),
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
            else:
                if question.cover:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "order": 1,
                        "answer": answer,
                        "image": question.cover,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
                else:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "order": 1,
                        "answer": answer,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
        else:
            resolution = Resolution.objects.get(patient=patientInstance, test=testInstance)
            if question.multipla:
                if question.cover:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "options": options,
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                        "image": question.cover
                    })
                else:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "options": options,
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                    })

            else:
                if question.cover:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                        "image": question.cover
                    })
                else:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                    })

    else:
        resolution = Resolution.objects.create(test=testInstance, patient=patientInstance)
        if question.multipla:
            if question.cover:
                return render(request, "pMentHa/perguntas/multipla.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "options": options,
                    "order": 1,
                    "image": question.cover,
                    "test": resolution.test.name
                })
            else:
                return render(request, "pMentHa/perguntas/multipla.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "options": options,
                    "order": 1,
                    "test": resolution.test.name
                })
        else:
            if question.cover:
                return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "order": 1,
                    "image": question.cover,
                    "test": resolution.test.name
                })
            else:
                return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "order": 1,
                    "test": resolution.test.name
                })
