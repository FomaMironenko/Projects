#include "pch.h"

#include <iostream>
#include <string>
#include <map>

#undef NDEBUG
#include <cassert>
#include <regex>

using namespace std;


const regex gex("([А-Яа-яёЁ_])([А-Яа-я0-9ёЁ_])*");

bool check_name(string name)
{
	return regex_match(name.begin(), name.end(), gex);
}


namespace MyLang
{

	struct Var
	{
		Var() = default;
		Var(string name)
		{
			assert(((void)"wrong name", check_name(name)));
			this->name = name;
			value.set_int(0);
		}
		Var(string name, int a)
		{
			assert(((void)"wrong name", check_name(name)));
			this->name = name;
			value.set_int(a);
			tp = INT;
		}
		Var(string name, double b)
		{
			assert(((void)"wrong name", check_name(name)));
			this->name = name;
			value.set_int(b);
			tp = DOB;
		}

		bool operator==(Var & other) { return this->name == other.name; }
		bool operator==(double & num) { return (tp == INT ? value.a : value.b) == num; }
		bool operator!=(double & num) { return (tp == INT ? value.a : value.b) != num; }
		bool operator> (double & num) { return (tp == INT ? value.a : value.b) > num; }
		bool operator< (double & num) { return (tp == INT ? value.a : value.b) < num; }

		Var & operator=(Var & other)
		{
			if (other.tp == INT)
			{
				this->tp = INT;
				value.set_int(other.value.a);
			}
			else
			{
				this->tp = DOB;
				value.set_dob(other.value.b);
			}
			return *this;
		}
		Var & operator=(Var && other) = default;
		Var & operator=(int x)
		{
			tp = INT;
			value.set_int(x);
			return *this;
		}
		Var & operator=(double x)
		{
			tp = DOB;
			value.set_dob(x);
			return *this;
		}

		union
		{
			void set_int(int _a) { a = _a; }
			void set_dob(double _b) { b = _b; }
			int a;
			double b;
		} value;

		enum type { INT, DOB } tp;

		string name;
	};



	struct Statement
	{
		virtual void print() = 0;
		virtual void execute() = 0;

		static map<string, Var> variables;
	};


	// declare имя
	struct Declaration : Statement
	{
		Declaration(string name) : name(name)
		{
			assert(((void)"wrong name", check_name(name)));
		}

		void print()
		{
			cout << "declare " << name << ";\n";
		}
		void execute()
		{
			assert(((void)"vriable already defined", variables.find(name) == variables.end()));
			variables[name] = Var(name); // оператор присваивания перемещением
		}

		~Declaration()
		{
			variables.erase(name);
		}

		string name;
	};


	//имя1 := имя2
	struct AssignName : Statement
	{
		AssignName(string name1, string name2) : name1(name1), name2(name2)
		{	}

		void print()
		{
			cout << name1 << " := " << name2 << ";\n";
		}
		void execute()
		{
			assert(((void)(name1 + " not defined"), variables.find(name1) != variables.end()));
			assert(((void)(name2 + " not defined"), variables.find(name2) != variables.end()));
			variables[name1] = variables[name2]; // оператор присваивания
		}

		string name1, name2;
	};


	// имя <оператор cравнения> число
	struct Comparison : Statement
	{
		Comparison(string name, const char* oper) : name(name), operation(oper)
		{
			assert(((void)"no such operation ", operation == "==" || operation == "!=" || operation == ">" || operation == "<"));
		}

		void print()
		{
			cout << " (" << name << " " << operation << ") ";
		}
		void execute()
		{
			abort();
		}
		bool execute_bool()
		{
			assert(((void)(name + " not defined"), variables.find(name) != variables.end()));
			if (operation == "==") { return variables[name] == num; }
			if (operation == "!=") { return variables[name] != num; }
			if (operation == ">") { return variables[name] > num; }
			if (operation == "<") { return variables[name] < num; }
		}

		double num;
		string operation;
		string name;
	};


	// имя := число
	struct AssignValue : Statement
	{
		AssignValue(string name, int x) : name(name), tp(INT)
		{
			value.set_int(x);
		}
		AssignValue(string name, double x) : name(name), tp(DOB)
		{
			value.set_dob(x);
		}

		void print()
		{
			cout << name << " := " << (tp == INT ? value.a : value.b) << ";\n";
		}
		void execute()
		{
			assert(((void)(name + " not defined"), variables.find(name) != variables.end()));
			variables[name] = (tp == INT ? value.a : value.b);
		}

		union
		{
			void set_int(int _a) { a = _a; }
			void set_dob(double _b) { b = _b; }
			int a;
			double b;
		} value;
		enum type { INT, DOB } tp;
		string name;
	};


	// {оператор1 оператор2}
	struct Compound : Statement
	{
		Compound(Statement* oper1, Statement* oper2) : oper1(oper1), oper2(oper2)
		{
			assert(((void)"wrong syntax", !dynamic_cast<Comparison*>(oper1)));
			assert(((void)"wrong syntax", !dynamic_cast<Comparison*>(oper2)));
		}

		void print()
		{
			cout << "{\n";
			oper1->print();
			oper2->print();
			cout << "}\n";
		}
		void execute()
		{
			oper1->execute();
			oper2->execute();
		}

		Statement *oper1, *oper2;
	};


	// if условие then оператор1 else оператор2
	struct Conditional : Statement
	{
		Conditional(Comparison* comp, Statement* oper1, Statement* oper2) : 
			oper1(oper1), oper2(oper2), comp(comp)
		{
			assert(((void)"wrong syntax", !dynamic_cast<Comparison*>(oper1)));
			assert(((void)"wrong syntax", !dynamic_cast<Comparison*>(oper2)));
		}

		void print()
		{
			cout << "if";
			comp->print();
			cout << "\n{\n";
			oper1->print();
			cout << "}\n";

			cout << "else\n{\n";
			oper2->print();
			cout << "}\n";
		}

		void execute()
		{
			if (comp->execute_bool())
			{
				oper1->execute();
			}
			else
			{
				oper2->execute();
			}
		}

		Comparison* comp;
		Statement *oper1, *oper2;
	};


	// while условие do оператор
	struct Loop : Statement
	{
		Loop(Comparison* comp, Statement* oper) : comp(comp), oper(oper)
		{
			assert(((void)"wrong syntax", !dynamic_cast<Comparison*>(oper)));
		}

		void print()
		{
			cout << "while";
			comp->print();
			cout << "\n{\n";
			oper->print();
			cout << "}\n";
		}
		void execute()
		{
			while (comp->execute_bool())
			{
				oper->execute();
			}
		}

		Comparison* comp;
		Statement* oper;
	};

}




int main()
{
	setlocale(LC_ALL, "Russian");

	
    return EXIT_SUCCESS; 
}