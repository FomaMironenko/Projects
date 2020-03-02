#include "pch.h"
#include <iostream>

#include <fstream>
#include <sstream>

#include <string>
#include <vector>
#include <map>
#include <set>

#include <algorithm>

using namespace std;

enum type
{ ter, non, var };


struct symbol
{
	symbol() = default;
	symbol(int num, type tp): num(num), tp(tp)
	{	}

	const type tp;
	int num;
};


struct terminal: symbol
{
	terminal(int n, string _name): symbol(n, ter)
	{	
		if (!isupper(_name[0]))
		{
			cout << "<Err> worng terminal name:   \t" << _name << endl;
		}
		transform(_name.begin(), _name.end(), _name.begin(), tolower);
		transform(_name.begin(), _name.begin() + 1, _name.begin(), toupper);
		name = _name;
	}

	string operator *()
	{
		return name;
	}

	string name;
};

struct nonterminal : symbol
{
	nonterminal(int n, string _name): symbol(n, non)
	{	
		if (isupper(_name[0]))
		{
			cerr << "<Err> worng nonterminal name:\t" << _name << endl;
		}
		transform(_name.begin(), _name.end(), _name.begin(), tolower);
		name = _name;
	}


	vector<symbol> rule;
	string name;
};

struct variable : symbol
{
	variable(int pos) : symbol(-1, var), pos(pos)
	{	}
	int pos;
	nonterminal* formula;
};


typedef pair<string, nonterminal> dct_non;
typedef pair<string, terminal>    dct_ter;


// описание правила замены
struct Substitution
{

	vector<symbol*> expr;
};


// хранение всех символов для текущей задачи
struct Symbols
{
	Symbols() = default;

	void add_non(int n, string name)
	{
		nonterminal tmp(n, name);
		if (nont.insert( dct_non(tmp.name, tmp) ).second == false)
		{
			cerr << "<Err> multiple initialisation of nonterminal:\t" << name << endl;
		}
		else { n_non++; }
	}
	void add_ter(int n, string name)
	{
		terminal tmp(n, name);
		if (term.insert( dct_ter(tmp.name, tmp) ).second == false)
		{
			cerr << "<Err> multiple initialisation of terminal:   \t" << name << endl;
		}
		else { n_ter++; }
	}

	void read_non(fstream & file)
	{
	string line;
	stringstream inp;
	string name;
	int num;
		getline(file, line);
		inp << line;
		while (!inp.eof())
		{
			if (inp >> name, inp >> num)
			{
				add_non(num, name);
			}
			else 
			{ 
				inp.clear();
				inp >> name;
				cerr << "<Err> wrong input format: nonterminals arg " << n_non << endl;
			}
		}
	}
	void read_ter(fstream & file)
	{
	string line;
	stringstream inp;
	string name;
	int num;
		getline(file, line);
		inp << line;
		while (!inp.eof())
		{
			if (inp >> name, inp >> num)
			{
				add_ter(num, name);
			}
			else 
			{ 
				inp.clear();
				inp >> name;
				cerr << "<Err> wrong input format: terminals arg " << n_ter << endl;
			}
		}
	}

	void prt_non()
	{
		cout << endl;
		for (auto it = nont.begin(); it != nont.end(); it++)
		{
			cout << it->first << ": " << it->second.num << endl;
		}
	}
	void prt_ter()
	{
		cout << endl;
		for (auto it = term.begin(); it != term.end(); it++)
		{
			cout << it->first << ": " << it->second.num << endl;
		}
	}

	map<string, const nonterminal> nont;
	map<string, const terminal>	   term;
	static int n_non;
	static int n_ter;
};
int Symbols::n_non = 0;
int Symbols::n_ter = 0;


int main()
{
	Symbols dict;
	fstream input("C:\\Users\\fomiu\\Desktop\\files_for_parsing\\input.txt");
	dict.read_non(input);
	dict.read_ter(input);
	dict.prt_non();
	dict.prt_ter();

    return EXIT_SUCCESS; 
}



// КС грамматика на деревьях
// деревянные языки
// tree-adjusting grammar
// lexicalized tree-adjoining grammar
// tree-substitution grammar

// https://www.intuit.ru/studies/courses/26/26/lecture/823?page=1

/*
Пусть есть два непересекающихся набора символов, терминальных и нетерминальных соответственно
(отличных от скобок, запятой и переменных), и каждому символу сопоставлено неотрицательное целое число.

Под термами понимаются следующие конструкции :
а) Любой символ, которому сопоставлено число 0, является термом.Такой терм называется константой.
б) Строка из любого символа, которому сопоставлено число n > 0, за ним открывающая скобка, затем n 
термов через запятую(эти термы называются фактическими параметрами), затем закрывающая скобка, 
тоже является термом.Такой терм называется вызовом того символа, который стоит в начале этой строки.
в) Любая переменная является термом.

Под правилом замены понимается правило, состоящее из левой части(нетерминальный символ, которому 
сопоставлено число n, за ним открывающая скобка, затем n различных переменных через запятую (эти 
переменные называются формальными параметрами), затем закрывающая скобка) и правой части (произвольный 
терм, в котором могут встречаться переменные только из левой части).

Если есть терм без переменных Т, в котором встречается вызов нетерминального символа A, и есть 
правило замены с вызовом символа А в левой части, то такой вызов A в составе Т может быть заменен 
на правую часть правила замены, причем формальные параметры принимают значения фактических(соответствие 
по номеру параметра в вызове).

Начальный символ--- нетерминальный символ, которому сопоставлено число 0. Окончательный терм--- терм 
без переменных и нетерминальных символов.

Теперь собственно задача.Имеется файл, в котором на первой строке имеется набор нетерминальных 
символов(представленных идентификаторами с маленькой буквы; начальный символ идет на этой строке первым), 
за каждым из которых указано соответствующее ему число(идентификаторы и числа разделяются пробелами).Аналогично, 
на второй строке указаны терминальные символы(идентификаторы с большой буквы и их числа).На третьей строке--- 
число правил замены, и на последующих строках сами правила по одному на строке(сначала левая часть, затем пробел 
и правая часть; переменные-- - идентификаторы, начинающиеся с символа подчеркивания).Наконец, после правил на последней 
строке-- - окончательный терм.Требуется вывести ответ("да" или "нет") на вопрос-- - можно ли получить окончательный 
терм при помощи нескольких замен описанного выше типа из начального нетерминального символа. Если ответ-- - "да", 
то на нескольких последующих строках нужно вывести термы, первый из которых-- - начальный нетерминальный символ, 
второй-- - результат первой замены, и т.д., последний-- - заданный окончательный терм.
*/
