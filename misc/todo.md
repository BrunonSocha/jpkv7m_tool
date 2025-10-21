# To do list
This list will be expanded if necessary.

## XLSX creation
# Basic data
- [x] Kod urzędu
- [x] Okres
- [x] Osoba niefizyczna
- [x] NIP
- [x] Pełna nazwa
- [x] Adres e-mail
- [x] Nr tel

# Sales
- [ ] Country code
- [ ] NIP
- [ ] Invoice number
- [ ] Invoice date
- [ ] K19 Netto value
- [ ] K20 22/23 VAT value

# Purchases
- [ ] Country code
- [ ] NIP
- [ ] Invoice number
- [ ] Invoice date
- [ ] K42 Netto value
- [ ] K43 VAT value

# Summary
- [ ] P39 should be automatic

## XML handling
- [ ] Create a new XML file in correct format, using the current date. 
- [ ] If no previous files are detected, prompt the user for the outstanding values from the previous month.
- [ ] Correctly input that data into the new file.
- [ ] Check file correctness.

## Additional steps
- [ ] English ver.

## Future rewrite
- Use *lxml* for xmls, validate them using *xmlschema*
- Introduce signing

---
## Sidenote
This project serves to aid my dad in tax reporting for our company, and as a revision of my Python skills (haven't touched Python in a long time). Because we don't use many of the functionalities of the JPK_V7M form, they won't be implemented at the beginning - with time I plan on expanding it - to handle different data, as well as handle JPK_V7K (or whatever the quarterly version is called).