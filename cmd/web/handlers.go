package main

import (
	"errors"
	"fmt"
	"html/template"
	"nestroh/pkg/models"
	"net/http"
)

func (app *application) home(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		app.notFound(w) // Использование помощника notFound()
		return
	}

	files := []string{
		"./ui/html/home.html",
	}

	ts, err := template.ParseFiles(files...)
	if err != nil {
		app.serverError(w, err) // Использование помощника serverError()
		return
	}

	err = ts.Execute(w, nil)
	if err != nil {
		app.serverError(w, err) // Использование помощника serverError()
	}
}

func (app *application) home2(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/home2" {
		app.notFound(w) // Использование помощника notFound()
		return
	}

	files := []string{
		"./ui/html/table.html",
	}

	ts, err := template.ParseFiles(files...)
	if err != nil {
		app.serverError(w, err) // Использование помощника serverError()
		return
	}

	err = ts.Execute(w, nil)
	if err != nil {
		app.serverError(w, err) // Использование помощника serverError()
	}

	model := "123"
	s, err := app.trunks.Get(model)
	if err != nil {
		if errors.Is(err, models.ErrNoRecord) {
			app.notFound(w)
		} else {
			app.serverError(w, err)
		}
		return
	}

	// Создаем экземпляр структуры templateData, содержащей данные заметки.
	data := &templateData{Trunk: s}
	// Передаем структуру templateData в качестве данных для шаблона.
	err = ts.Execute(w, data)
	if err != nil {
		app.serverError(w, err)
	}

}

func (app *application) showTable(w http.ResponseWriter, r *http.Request) {
	model := r.URL.Query().Get("model")
	if model != "0" {
		s, err := app.trunks.Get(model)
		if err != nil {
			if errors.Is(err, models.ErrNoRecord) {
				app.notFound(w)
			} else {
				app.serverError(w, err)
			}
			return
		}
		// Создаем экземпляр структуры templateData, содержащей данные заметки.
		data := &templateData{Trunk: s}

		files := []string{
			"./ui/html/table.html",
		}

		ts, err := template.ParseFiles(files...)
		if err != nil {
			app.serverError(w, err)
			return
		}

		// Передаем структуру templateData в качестве данных для шаблона.
		err = ts.Execute(w, data)
		if err != nil {
			app.serverError(w, err)
		}
	} else {
		files := []string{
			"./ui/html/table_start.html",
		}

		ts, err := template.ParseFiles(files...)
		if err != nil {
			app.serverError(w, err) // Использование помощника serverError()
			return
		}

		err = ts.Execute(w, nil)
		if err != nil {
			app.serverError(w, err) // Использование помощника serverError()
		}
	}
}

func (app *application) createTable(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.Header().Set("Allow", http.MethodPost)
		app.clientError(w, http.StatusMethodNotAllowed)
		return
	}
	/*
		http://www.jetsource.ru/scripts/javascript_jquery/otpravka_post_i_get_zaprosov

		надо почитать
	*/
	// Создаем несколько переменных, содержащих тестовые данные. Мы удалим их позже.
	Model := "A-B4"
	ParamCharge := 56
	ParamQn := 8.6
	ParamQg := 8.6
	ParamQv := 8.6
	P := 8.6
	T := 8.6
	ParamFlowRegime := "\u0430\u043d\u0442\u0438\u043a\u043e\u0440\u0440\u043e\u0437\u0438\u0439\u043d\u044b\u0439"
	ParamFacticVelocity := 10
	ParamCriticVelocity := 15
	ParamCrash := 36
	ParamLifetime := 16
	ResidualResource := 10

	// Передаем данные в метод SnippetModel.Insert(), получая обратно
	// ID только что созданной записи в базу данных.
	id, err := app.trunks.Insert(Model, ParamCharge, ParamQn,
		ParamQg,
		ParamQv,
		P,
		T,
		ParamFlowRegime,
		ParamFacticVelocity,
		ParamCriticVelocity,
		ParamCrash,
		ParamLifetime,
		ResidualResource)

	if err != nil {
		app.serverError(w, err)
		return
	}

	// Перенаправляем пользователя на соответствующую страницу заметки.
	http.Redirect(w, r, fmt.Sprintf("/table?model=%d", id), http.StatusSeeOther)
}
