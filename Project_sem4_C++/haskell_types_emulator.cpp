#include "pch.h"
#include <iostream>

#include <string>
#include <vector>
#include <map>

#undef NDEBUG
#include <cassert>

using namespace std;


struct Type;
struct InlineTy;
struct VarTy;
struct ListTy;
struct FuncTy;
struct CortTy;



struct Type
{
	virtual Type* clone() = 0;
	virtual void  logic() = 0;
	/* return: true if empty
	   arr   : true if empty */
	virtual bool  empty(bool[26]) = 0;
	virtual void  print() = 0;

	virtual ~Type() = default;
};


struct InlineTy: Type
{
	enum { T = 0, Bot = 1} TY;

	InlineTy()
	{
		this->TY = Bot;
	}
	InlineTy(bool empty)
	{
		this->TY = empty ? Bot : T;
	}

	Type* clone()
	{
		return new InlineTy(this->TY);
	}
	void logic()
	{
		if (this->TY == Bot) cout << "Bot";
		else cout << "T";
	}
	void print()
	{
		if (this->TY == Bot) cout << "Bot";
		else cout << "T";
	}
	bool empty(bool vals[26])
	{
		return this->TY == Bot;
	}

	~InlineTy() = default;
};



struct VarTy: Type
{
	VarTy(char _name, Type* value = nullptr)
	{
		assert(((void)"Wrong variable name", int(_name) >= 97 && int(_name) <= 122));
		name = _name;
		if (vars.find(name) == vars.end())
		{
			vars[name] = value == nullptr ? new InlineTy(InlineTy::Bot) : value->clone();
		}
	}

	static int id(char name)
	{
		return int(name) - 97;
	}

	void setVal(Type* value)
	{
		if(value != nullptr) vars[name] = value->clone();
	}

	Type* clone()
	{
		return new VarTy(name);
	}
	void logic()
	{
		cout << name;
	}
	void print()
	{
		vars[name]->print();
	}
	bool empty(bool vals[26])
	{
		return vals[id(name)];
	}

	~VarTy() = default;

	char name;
	static map<char, Type*> vars;
};

map<char, Type*> VarTy::vars = map<char, Type*>();


// elements with same type
struct ListTy: Type
{
	ListTy() : n(0), type(nullptr)
	{	}
	ListTy(Type* source, unsigned n): n(n), type(source->clone())
	{	}

	Type* clone()
	{
		return new ListTy(type, n);
	}
	void logic()
	{
		if (n == 0)
		{
			cout << "Bot";
			return;
		}
		cout << "[ " << n << " : ";
		type->logic();
		cout << " ]";
	}
	void print()
	{
		if (n == 0)
		{
			cout << "[ ]";
			return;
		}
		cout << "[ " << n << " : ";
		type->print();
		cout << " ]";
	}
	bool empty(bool vals[26])
	{
		if (n == 0)
		{
			return true;
		}
		return type->empty(vals);
	}

	~ListTy()
	{
		delete type;
	}

	Type* type;
	unsigned n;
};



struct FuncTy: Type
{
	FuncTy(Type* _from, Type* _to)
	{
		from = _from->clone();
		to = _to->clone();
	}

	Type* clone()
	{
		return new FuncTy(from, to);
	}
	void logic()
	{
		cout << "{ ";  from->logic(); cout << " }";
		cout << " => ";
		cout << "{ ";  to->logic(); cout << " }";
	}
	void print()
	{
		cout << "{ ";  from->print(); cout << " }";
		cout << " -> ";
		cout << "{ ";  to->print(); cout << " }";
	}
	bool empty(bool vals[26])
	{
		bool ef = !from->empty(vals);
		bool et = !to->empty(vals);
		return !(!ef || et);
	}

	~FuncTy()
	{
		delete from;
		delete to;
	}

	Type* from;
	Type* to;
};


struct CortTy: Type
{
	CortTy(vector<Type*> source)
	{
		for (auto it = source.begin(); it < source.end(); it++)
		{
			tyCort.push_back((*it)->clone());
		}
	}

	Type* clone()
	{
		return new CortTy(tyCort);
	}
	void logic()
	{
		cout << "( ";
		for (int i = 0; i < tyCort.size() - 1; i++)
		{
			tyCort[i]->logic();
			cout << " && ";
		}
		tyCort.back()->logic();
		cout << " )";
	}
	void print()
	{
		cout << "( ";
		for (int i = 0; i < tyCort.size() - 1; i++)
		{
			tyCort[i]->print();
			cout << " , ";
		}
		tyCort.back()->print();
		cout << " )";
	}
	bool empty(bool vals[26])
	{
		if (tyCort.size() == 0)
		{
			return true;
		}
		for (auto it = tyCort.begin(); it < tyCort.end(); it++)
		{
			if ((*it)->empty(vals))
			{
				return true;
			}
		}
		return false;
	}

	~CortTy()
	{
		for (auto it = tyCort.begin(); it < tyCort.end(); it++)
		{
			delete *it;
		}
	}

	vector<Type*> tyCort;
};




void test1()
{
	bool arr[26] = { false };

	InlineTy T(InlineTy::T);
	InlineTy B(InlineTy::Bot);

	CortTy C({ &T, &T, &B });

	FuncTy F(&C, &T);

	FuncTy F1(&F, &F);

	C.print();
	cout << endl;
	F1.print();
	cout << endl;
	F1.logic();
	cout << endl;
	cout << F1.empty(arr);
}

// variables
void test2()
{
	InlineTy T(InlineTy::T);
	InlineTy B(InlineTy::Bot);

	VarTy a('a', &T);
	VarTy b('a');
	b.setVal(&B);
	a.print();
	cout << endl;

	CortTy C({ &a, &b });
	C.print();

}

void test3()
{
	bool arr[26] = { false };

	InlineTy T(InlineTy::T);
	InlineTy B(InlineTy::Bot);

	VarTy a('a', &T);
	VarTy b('a');
	arr[VarTy::id(a.name)] = true;

	CortTy C({ &a, &b });
	a.logic(); 
	cout << endl << a.empty(arr) << endl << endl;
	C.logic();
	cout << endl;
	cout << C.empty(arr);
}

void test4()
{
	bool arr[26] = { false };

	InlineTy T(InlineTy::T);
	InlineTy B(InlineTy::Bot);
	
	ListTy L(&T, 3);
	VarTy a('a');
	CortTy C({ &a, &T });
	FuncTy F(&L, &C);
	
	F.print();
	cout << endl << endl;
	arr[VarTy::id(a.name)] = true;

	a.logic();
	cout << endl << a.empty(arr) << endl << endl;

	F.logic();
	cout << endl << F.empty(arr) << endl;
}


int main()
{
	cout << "TEST1\n";
	test1();
	cout << "\n---------------------------------------------\n\n\n";

	cout << "TEST2\n";
	test2();
	cout << "\n---------------------------------------------\n\n\n";

	cout << "TEST3\n";
	test3();
	cout << "\n---------------------------------------------\n\n\n";

	cout << "TEST4\n";
	test4();
	cout << "\n---------------------------------------------\n\n\n";

	return EXIT_SUCCESS;
}