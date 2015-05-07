var inputObj = document.getElementById("input");
            var outputObj = document.getElementById("output");

            inputObj.addEventListener("click", clearOutputField);

            $(document).ready(function() {
                 var aTags =["Supporting Arts & Culture", "Improving Education", "Protecting the Environment", "Animal Welfare", "Improving Health Care", "Women's Health", "Mental Health", "Suicide Prevention", "Diseases", "Curing Cancer", "Curing Breast Cancer", "HIV & Aids", "Autism", "Children's Diseases", "Justice", "Trafficking and Exploitation", "Increasing Jobs", "Feeding the Hungry", "Improving Nutrition", "Affordable Housing", "Disaster Relief", "Recreation & Fitness", "At-Risk Youth", "Domestic Violence Shelters & Services", "Supporting Services for Seniors", "International Economic Development", "International Disaster Relief", "International Social Justice", "Civil Rights & Liberties", "Women's Rights", "LGBT Rights", "Reproductive Rights", "Community Economic Development", "Advancing Science & Technology", "Services for Vets", "Sports", "Skip", "Unclear", "None of the above"];

                $( "#input" ).autocomplete({
                    source: aTags,
                    select: function (event, ui) { populateOutputField(event, ui) }
                });
            });

            function clearOutputField() {
                inputObj.value = '';
                outputObj.value = '';
            };

            function populateOutputField(event, ui) {
                var selectedObj = ui.item;
                var output = selectedObj.value;

                outputObj.value = output;

                var md5 = "{{ article.md5 }}"
                $.ajax({
                  type: "POST",
                  url: '/',
                  data: {id7: md5}
                });

                $.ajax({
                  type: "POST",
                  url: '/',
                  data: {id: output}
                });
            };
