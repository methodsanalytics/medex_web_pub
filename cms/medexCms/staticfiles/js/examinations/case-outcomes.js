(function ($) {

    var CaseOutcomePage = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    CaseOutcomePage.prototype = {
        setup: function() {
            this.hasChanges = false;
            this.changedForm = null;
            this.scrutinyCompleteForm = new ScrutinyCompleteForm(this.wrapper.find('#scrutiny-form'),
                                            this.setHasChanges.bind(this));
            this.coronerReferralForm = new CoronerReferralForm(this.wrapper.find('#coroner-referral-form'),
                                            this.setHasChanges.bind(this));
            this.tabChangeModal = new ChangeTabModal($('#tab-change-modal'), this.forceSave.bind(this));
            this.initialiseTabs();
        },

        initialiseTabs: function () {
          this.tabBlock = new TabBlock(this.wrapper.find('.examination__tab-bar'), this.getHasChanges.bind(this), this.tabChangeModal);
        },

        getHasChanges: function() {
            return this.hasChanges;
        },

        setHasChanges: function(value, form) {
            this.hasChanges = value;
            this.changedForm = form;
        },

        forceSave: function (nextTab) {
          this.changedForm.form[0].action += '?nextTab=' + nextTab;
          this.changedForm.form.submit();
        }
    }

    var ScrutinyCompleteForm = function (form, changeCallback) {
        this.form = $(form);
        this.changeCallback = changeCallback;
        this.setup();
    }

    ScrutinyCompleteForm.prototype = {
        setup: function () {
            this.checkBox = new Input(this.form.find('input#scrutiny-confirmation'), this.handleChange.bind(this));
            this.btn = this.form.find('button#confirm-scrutiny-button');

            this.setInitialView();
        },

        setInitialView: function() {
            this.btn.attr("disabled", true);
        },

        handleChange: function() {
            if (this.checkBox.isChecked()) {
                this.btn.attr("disabled", false);
                this.changeCallback(true, this);
            } else {
                this.btn.attr("disabled", true);
                this.changeCallback(false, null);
            }
        }
    }

    var CoronerReferralForm = function(form, changeCallback) {
        this.form = $(form);
        this.changeCallback = changeCallback;
        this.setup();
    }

    CoronerReferralForm.prototype = {
        setup: function() {
            this.checkBox = new Input(this.form.find('#coroner-referral-confirmation'), this.handleChange.bind(this));
            this.saveBar = this.form.find('.sticky-save');
        },

        handleChange: function() {
            if (this.checkBox.isChecked()) {
                this.toggleSaveBar();
                this.changeCallback(true, this);
            } else {
                this.toggleSaveBar();
                this.changeCallback(false, null);
            }
        },

        toggleSaveBar: function () {
            this.saveBar.toggle();
        }
    }

    function init() {
        var caseOutcome = $('.examination__edit');
        for (var i = 0; i < caseOutcome.length; i++) {
            new CaseOutcomePage(caseOutcome[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
